import itertools
import sys
import traceback

import cv2
import dask
import dask.array as da
import numpy as np
import pandas as pd
import scipy.ndimage as ndi
import sep
from dask import delayed
from owl_dev.logging import logger

from ..typing_utils import NumArray


def create_mask(
    image: NumArray,
    cl_morph_parm=10,
    c_min_area=0.0009,
    c_count_max=15,
    output_size=None,
):

    """Create mask from the scaled image

    Parameters
    ----------
    image
        input image (better to be an scaled image)
    cl_morph_parm
        cv2.MORPH_ELLIPSE parameter for the Morphological closing
    c_min_area
        min area (relative to the full field area) for a contour to be considered as mask
    c_count_max
        Maximum number of contours to be checked for being mask
    output_size
        output image size

    Returns
    -------
    output
        Mask image with mask values set to 1 and background values set to 0
    """

    # to avoid compressing all background values around 0, and dealing with
    # zero values for background, we scale data to 25 and and add 1 later
    image = ((image - image.min()) / (image.max() - image.min()) * 254) + 1.0

    # apply close morphology to get rid of small structures and make the big blog bolder
    # change the kernel to (5,5) if background is still noisy
    image = cv2.blur(image, (3, 3))
    outer = cv2.morphologyEx(
        image,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cl_morph_parm, cl_morph_parm)),
    )

    # fill/replace zeros with median value to have smoother background
    # then we apply blur filter to remove any artificial casued by filling with median
    outer[outer <= 1] = np.median(outer[outer > 1])
    outer = outer.astype(np.uint8)
    outer = cv2.blur(outer, (5, 5))

    # remove noise by filtering the most frequent element from the image
    ret, th1 = cv2.threshold(
        outer, np.median(outer), 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE
    )

    # binaries the image and fill the holes
    image_fill_holes = ndi.binary_fill_holes(th1).astype(np.uint8)

    cnts, _ = cv2.findContours(
        image_fill_holes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    # create an empty mask image
    mask = np.zeros(image.shape, np.uint8)

    # assuming the min area for tissue is (e.g. 0.0009 = 0.03x * 0.03y)
    min_blob_area = c_min_area * image.shape[1] * image.shape[0]
    blob_counter = 0

    # sort contours by area (large to small) and then loop over them and select those with specific characteristics
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for cnt in cnts[: np.min([int(c_count_max), len(cnts)])]:
        if cv2.contourArea(cnt) > min_blob_area:
            blob_counter += 1
            cv2.drawContours(mask, [cnt], -1, 255, cv2.FILLED)
            mask = cv2.bitwise_and(image_fill_holes, mask)

    if output_size is not None:
        mask = cv2.resize(mask, dsize=output_size, interpolation=cv2.INTER_LINEAR)

    return mask


def run_sep(
    indx,
    im,
    mask,
    overlap_size=200.0,
    chunk_loc=None,
    bw=128,
    bh=128,
    minarea=880,
    deblend_nthresh=2,
    circularity=0.9,
    std_l16=None,
):

    if chunk_loc is None:
        chunk_loc = [[np.nan, np.nan], [np.nan, np.nan]]

    im = np.array(im)
    mask = np.array(mask).astype(bool)

    extc_bkg = sep.Background(im, mask=mask, bw=bw, bh=bh)

    logger.debug(
        "Background: %f - Global RMS: %f", extc_bkg.globalback, extc_bkg.globalrms
    )

    # subtract the background
    reduced_data = im - extc_bkg.back()
    # here you could introduce as many detection-thresholds as you want to give a try
    threshold_0 = max(0, np.mean(reduced_data[np.invert(mask)])) + (
        1.3 * np.std(extc_bkg.back())
    )
    threshold_1 = max(0, np.mean(reduced_data[np.invert(mask)])) + (
        1.8 * np.std(extc_bkg.back())
    )
    threshold_2 = max(0, np.mean(reduced_data[np.invert(mask)])) + (
        2.3 * np.std(extc_bkg.back())
    )
    threshold_3 = max(0, np.mean(reduced_data[np.invert(mask)])) + (
        3.0 * np.std(extc_bkg.back())
    )
    threshold_4 = max(0, np.mean(reduced_data[np.invert(mask)])) + (1.5 * std_l16)
    threshold_list = [threshold_0, threshold_1, threshold_2, threshold_3, threshold_4]

    try:
        for i_th, thr_i in enumerate(threshold_list):
            try:
                # detect objects (try 1): Using the local (block) bacground

                objects = sep.extract(
                    reduced_data,
                    thr_i,
                    minarea=minarea,
                    deblend_nthresh=deblend_nthresh,
                    mask=mask,
                    segmentation_map=False,
                )
                break
            except Exception:
                objects = None
                if i_th < len(threshold_list) - 1:
                    continue
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        logger.debug("".join(lines))
        return None

    if objects is None:
        logger.debug("No objects found")
        return pd.DataFrame()

    objects_df = pd.DataFrame(objects)

    objects_df = objects_df[
        (objects_df["flag"] == 0) & (objects_df["b"] / objects_df["a"] > circularity)
    ]

    # add indx and x(y)_range of each chunk to the dataframe
    df_len = len(objects_df)
    objects_df.insert(0, "indx_0", indx[0])
    objects_df.insert(1, "indx_1", indx[1])
    objects_df.insert(2, "X_RANGE_i", chunk_loc[1][0])
    objects_df.insert(3, "X_RANGE_f", chunk_loc[1][1])
    objects_df.insert(4, "Y_RANGE_i", chunk_loc[0][0])
    objects_df.insert(5, "Y_RANGE_f", chunk_loc[0][1])
    objects_df.rename({"x": "x_block", "y": "y_block"}, axis=1, inplace=True)

    # estimate absolute coordinates of the peaks and keep them as new columns
    # called x and y (also corrected for overlapping)
    # Here we use (2 * index +1) * overlap_size factor to convert coordinates
    # from overlapped to the original (non-overlapped)

    if df_len > 0:

        fn_x = (
            lambda row: row.X_RANGE_i
            + row.x_block
            - (2.0 * row.indx_1 + 1) * overlap_size
        )

        col_x = objects_df.apply(fn_x, axis=1)
        objects_df = objects_df.assign(x=col_x.values)

        fn_y = (
            lambda row: row.Y_RANGE_i
            + row.y_block
            - (2.0 * row.indx_0 + 1) * overlap_size
        )

        col_y = objects_df.apply(fn_y, axis=1)
        objects_df = objects_df.assign(y=col_y.values)

        # TODO: more accurate way to estimate the radius
        fn_r = (lambda row: np.sqrt(row.a ** 2 + row.b ** 2) / 2)
        col_r = objects_df.apply(fn_r, axis=1)
        objects_df = objects_df.assign(r=col_r.values)

    else:
        objects_df["x"] = []
        objects_df["y"] = []
        objects_df["r"] = []

    logger.debug("Number of detected objects: %s (try: %d)", df_len, i_th + 1)

    return objects_df


@delayed
def compute_background_l16(image_l16: NumArray, mask_l16: NumArray, bw=128, bh=128):
    try:
        l16_bkg = sep.Background(image_l16, mask=mask_l16, bw=128, bh=128)
        std_l16 = np.std(l16_bkg.back())
    except Exception:
        std_l16 = np.nanquantile(image_l16[mask_l16 == 0], 0.75)
    return std_l16


def bead_detect_worker(image, mask, image_l16, mask_l16, overlap_size=0.0):

    # Evaluate standard deviation of background extracted from l16
    # In case the original background failed, we deploy this value
    std_l16 = compute_background_l16(image_l16, mask_l16, bw=128, bh=128)

    if overlap_size > 0.0:
        # add overlap to data and mask (for mask, we refill the boundary with 1 [equivalent to mask=True])
        image = da.overlap.overlap(image, overlap_size, {0: 1, 1: 1})
        mask = da.overlap.overlap(mask, overlap_size, {0: 1, 1: 1})

    beads_df = []
    for indx in itertools.product(*map(range, image.blocks.shape)):

        # extract the location of each chunk (overlapped) and later,
        # pass it to the run_sep function to be included in the results
        i, j = indx[-2:]
        chunk_loc_indx = [
            [sum(image.chunks[-2][:i]), sum(image.chunks[-2][: i + 1])],
            [sum(image.chunks[-1][:j]), sum(image.chunks[-1][: j + 1])],
        ]

        circ_chunk_i = delayed(run_sep)(
            indx,
            image.blocks[indx],
            mask.blocks[indx],
            overlap_size=overlap_size,
            chunk_loc=chunk_loc_indx,
            std_l16=std_l16,
        )

        if circ_chunk_i is not None:
            beads_df.append(circ_chunk_i)

    final_beads = dask.compute(beads_df)[0]
    final_beads = pd.concat(final_beads, ignore_index=True)

    return final_beads


def plot_beads(image, mask, beads_df, fig_fname=None):

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Ellipse
    except ModuleNotFoundError:
        logger.warning("matplotlib not found, cannot plot beads")
        return

    fig = plt.figure(figsize=(12, 8))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(np.array(mask), cmap="gray")
    ax1.set_title("Mask image")

    ax2 = fig.add_subplot(1, 2, 2)
    image = np.array(image)

    m, s = np.mean(image), np.std(image)
    ax2.imshow(image, interpolation="nearest", cmap="gray", vmin=m - s, vmax=m + s)
    ax2.set_title("Detected Beads")
    # plot an ellipse for each object
    for i in range(len(beads_df)):
        try:
            # plot boarder or each ellipse
            e = Ellipse(
                xy=(beads_df["x"][i], beads_df["x"][i]),
                width=6 * beads_df["a"][i],
                height=6 * beads_df["b"][i],
                angle=beads_df["theta"][i] * 180.0 / np.pi,
            )
            e.set_facecolor("none")
            e.set_edgecolor("red")
            ax2.add_artist(e)

            # mark the centre of each ellipse
            e_cent = Ellipse(
                xy=(beads_df["x"][i], beads_df["x"][i]),
                width=0.5 * beads_df["a"][i],
                height=0.5 * beads_df["b"][i],
                angle=beads_df["theta"][i] * 180.0 / np.pi,
            )
            e_cent.set_facecolor("none")
            e_cent.set_edgecolor("blue")
            ax2.add_artist(e_cent)

        except Exception:
            pass

    if fig_fname is not None:
        plt.tight_layout()
        plt.savefig(fig_fname)
        plt.close()

    else:
        plt.show()


# TODO: write as script
# if __name__ == "__main__":
