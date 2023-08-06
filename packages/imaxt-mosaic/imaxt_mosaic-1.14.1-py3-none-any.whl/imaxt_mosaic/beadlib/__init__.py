import itertools

import dask
import dask.array as da
import numpy as np
import pandas as pd
import xarray as xr
from dask import delayed
from owl_dev.logging import logger
from scipy.stats import median_abs_deviation
from skimage.transform import rescale

from ..settings import Settings
from ..utils import restart_workers, trim_memory_workers
from .detect import detect_beads


@delayed
def get_stats_nop(img):
    img = rescale(img.astype("float"), 0.25)
    mask = img.ravel() > 0
    if sum(mask) < img.size // 4:
        return 0, 0
    good = img.flatten()[mask]
    med = np.median(good)
    mad = median_abs_deviation(good)
    return med, mad


@delayed
def get_stats(img, nsamples=1000):
    median = []
    mad = []
    for n in range(nsamples):
        i, j = (np.random.uniform(size=2) * img.shape).astype("int")
        cutout = img[i - 50 : i + 50, j - 50 : j + 50]
        if cutout.size < 10000:
            continue
        cutout = cutout.atype("float")
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


def beads(output_path, overwrite=False):  # noqa: C901
    """Detect beads in a given image."""
    (output_path / "bead").mkdir(exist_ok=True)

    ds = xr.open_zarr(output_path / "mos")
    sections = list(ds)
    if Settings.sections:
        sections = [sections[i - 1] for i in Settings.sections]

    logger.info(f"{len(sections)} section(s) to proceed with")

    for sect in sections:
        output_bead = output_path / "bead" / f"{sect}.parquet"
        if output_bead.exists() and not overwrite:
            logger.info(f"Skipping section {sect}")
            continue

        all_df = []
        for zval in ds[sect].z.values:
            logger.debug(f"Processing section {sect}:Z{zval}")
            im = ds[sect].sel(z=zval).data.mean(axis=0)

            nim = im.rechunk((512, 512))
            stats = []
            for indx in itertools.product(*map(range, nim.blocks.shape)):
                stats.append(get_stats_nop(nim.blocks[indx]))
            stats = dask.compute(stats)[0]
            stats = sorted(stats, key=lambda x: (x[0] == 0) * 1e10 + x[1])
            med = np.median([s[0] for s in stats if s[0] > 0])
            mad = np.median([s[1] for s in stats if s[0] > 0])
            logger.debug("Image background stats median %f, mad %f", med, mad)

            fut = []
            im_o = da.overlap.overlap(im, 200, {0: 1, 1: 1})
            for indx in itertools.product(*map(range, im_o.blocks.shape)):
                fut.append(
                    detect_beads(
                        im_o.blocks[indx],
                        min_radius=Settings.beads["min_radius"],
                        max_radius=Settings.beads["max_radius"],
                        min_separation=Settings.beads["min_separation"],
                        min_area=Settings.beads["min_area"],
                        max_area=Settings.beads["max_area"],
                        threshold=Settings.beads["threshold"],
                        stats=(med, mad),
                    )
                )

            circles = dask.compute(fut)[0]
            circles_full = []
            dy, dx = im.chunksize
            for j, indx in enumerate(itertools.product(*map(range, im_o.blocks.shape))):
                c = circles[j]
                if c is None:
                    continue
                c[:, 0] = c[:, 0] - 200 + dx * indx[1]
                c[:, 1] = c[:, 1] - 200 + dy * indx[0]
                circles_full.append(c)

            try:
                beads = np.concatenate(circles_full)
            except ValueError:
                logger.warning("No beads detected in section %s", sect)
                continue

            df = pd.DataFrame(
                beads,
                columns=["x", "y", "radius", "amplitude", "x_fwhm", "y_fwhm", "theta"],
            )

            df["z"] = zval
            df["section"] = str(sect)
            logger.info(
                "Bead detection done for section %s:Z%d (%d)", sect, zval, len(df)
            )
            all_df.append(df)

        df = pd.concat(all_df, ignore_index=True)
        df.to_parquet(output_bead)

        # This should be done properly (with timeouts)
        trim_memory_workers()
        restart_workers()
