import warnings

import cv2
import numpy as np
import scipy.ndimage as ndi
from astropy.modeling import fitting, models
from dask import delayed
from owl_dev.logging import logger
from scipy.stats import median_abs_deviation
from skimage.transform import rescale


def get_stats(img, nsamples=1000):
    median = []
    mad = []
    for n in range(nsamples):
        i, j = (np.random.uniform(size=2) * img.shape).astype("int")
        cutout = img[i - 50 : i + 50, j - 50 : j + 50]
        if cutout.size < 10000:
            continue
        v1 = np.median(cutout)
        v2 = median_abs_deviation(cutout.ravel(), scale="normal")
        if not np.isnan(v1):
            if v1 > 0:
                median.append(v1)
                mad.append(v2)

    if len(median) > 10:
        z1 = np.percentile(median, 20)
        try:
            z2 = np.percentile([v2 for v1, v2 in zip(median, mad) if v1 < z1], 90)
        except Exception:
            z2 = 0
    else:
        z1 = z2 = 0
    return z1, z2


def compute_background(img, filter_size=256):
    med1 = ndi.median_filter(img, (1, filter_size))
    med2 = ndi.median_filter(img, (filter_size, 1))
    return (med1 + med2) / 2


def compute_mask(img, threshold, background=None):

    if background is not None:
        img = img - background

    # z1, z2 = get_stats(img)
    # if (z1 == 0) or (z2 == 0):
    #     return None

    img = ndi.gaussian_filter(img, (3, 3))

    mask = img > 1.5 * threshold  # z1 + threshold * z2

    mask = ndi.binary_fill_holes(mask)
    mask = ndi.binary_opening(mask, iterations=10)

    mask = (
        ndi.binary_dilation(mask, iterations=3) * 1
        - ndi.binary_erosion(mask, iterations=3) * 1
    )
    mask = ndi.binary_fill_holes(mask)

    mask = mask * 255

    mask = ndi.gaussian_filter(mask, 3)
    if mask.max() > 0:
        mask = mask / mask.max() * 255

    mask = mask.astype("uint8")
    return mask


@delayed
def detect_beads(  # noqa: C901
    img,
    min_separation=60,
    min_radius=60,
    max_radius=150,
    min_area=3_000,
    max_area=50_000,
    threshold=6,
    stats=None,
):
    """Detect beads in image using HoughCircles"""
    img = img.astype("float32")
    img = ndi.gaussian_filter(img, (3, 3))

    r_img = rescale(img, 0.25)
    r_background = compute_background(r_img)
    background = rescale(r_background, 4)

    mask = img > stats[0] + threshold * stats[1]
    mask = ndi.binary_fill_holes(mask)

    mask = (mask * 255).astype("uint8")
    analysis = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_16U)
    (totalLabels, label_ids, values, centroid) = analysis

    output = np.zeros(mask.shape, dtype="uint8")
    for i in range(1, totalLabels):
        area = values[i, cv2.CC_STAT_AREA]
        if area < 50_000:
            continue
        componentMask = (label_ids == i).astype("uint8") * 255
        # Creating the Final output mask
        output = cv2.bitwise_or(output, componentMask)
    mask_bg = output

    mask = img - background > threshold * stats[1]
    mask = np.maximum(mask * 255, mask_bg) > 0
    mask = ndi.binary_fill_holes(mask)

    mask = (
        ndi.binary_dilation(mask, iterations=10) * 1
        - ndi.binary_erosion(mask, iterations=10) * 1
    )
    mask = ndi.binary_fill_holes(mask)
    mask = ndi.binary_opening(mask, iterations=1)

    mask = (mask * 255).astype("uint8")
    analysis = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_16U)
    (totalLabels, label_ids, values, centroid) = analysis

    output = np.zeros(mask.shape, dtype="uint8")
    for i in range(1, totalLabels):
        area = values[i, cv2.CC_STAT_AREA]
        if (area < min_area) or (area > max_area):
            continue
        componentMask = (label_ids == i).astype("uint8") * 255
        # Creating the Final output mask
        output = cv2.bitwise_or(output, componentMask)
    mask = output

    circles0 = cv2.HoughCircles(
        mask,
        cv2.HOUGH_GRADIENT,
        1,
        min_separation,
        param1=150,
        param2=15,
        minRadius=min_radius,
        maxRadius=max_radius,
    )
    if circles0 is None:
        return None

    circles0 = np.round(circles0[0, :]).astype("int")
    p_init = models.Gaussian2D()
    fit_p = fitting.LevMarLSQFitter()
    if len(circles0) > 200:
        logger.warning("Too many beads detected in image %d", len(circles0))

    circles = []
    buffer = 10
    for c in circles0:
        xc, yc, rad = c
        rad = rad + buffer
        y, x = np.mgrid[: (2 * rad), : (2 * rad)]
        sy = slice(yc - rad, yc + rad)
        sx = slice(xc - rad, xc + rad)
        im = img[sy, sx]
        if im.size < (4 * rad * rad):
            continue
        if np.isnan(im).any():
            continue
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", module="astropy.modeling.fitting")
            try:
                p = fit_p(p_init, x, y, im)
            except Exception:
                logger.warning("Ignoring error fitting bead")
                continue
            fwhm = (p.x_fwhm + p.y_fwhm) / 2
            if fwhm > 300:
                continue
            if abs(p.x_fwhm - p.y_fwhm) > rad / 2:
                continue
            c = [
                xc,
                yc,
                rad - buffer,
                p.amplitude.value,
                p.x_fwhm,
                p.y_fwhm,
                p.theta.value,
            ]
            circles.append(c)
    if len(circles) > 0:
        circles = np.array(circles)
    else:
        circles = None
    return circles
