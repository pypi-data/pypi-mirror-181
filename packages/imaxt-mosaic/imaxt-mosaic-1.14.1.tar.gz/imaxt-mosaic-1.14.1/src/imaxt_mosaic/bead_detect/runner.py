import dask.array as da
import pandas as pd
import xarray as xr
from dask import delayed
from owl_dev.logging import logger
import cv2
import numpy as np
from ..settings import Settings
from ..utils import restart_workers, trim_memory_workers
from .bead_detector import bead_detect_worker, create_mask, plot_beads


def bead_detect(output_path, overwrite=False, fig=False):
    """Detect beads in a given image."""
    mod_input_path = output_path / "mos"
    (output_path / "bead").mkdir(exist_ok=True)

    ds = xr.open_zarr(mod_input_path)
    ds16 = xr.open_zarr(mod_input_path, group="l.16")
    sections = list(ds)
    if Settings.sections:
        sections = [sections[i - 1] for i in Settings.sections]

    logger.info(f"{len(sections)} section(s) to proceed with")

    for sect in sections:
        output_bead = output_path / "bead" / f"{sect}.parquet"
        if output_bead.exists() and not overwrite:
            logger.info(f"Skipping section {sect}")
            continue
        logger.info(f"Processing section {sect}")

        # loop over all available z planes
        all_bead_z = []
        for iz_sect, z_sect in enumerate(ds[sect]["z"].data):
            mean_data_org = ds[sect].sel(z=z_sect).mean("channel").data
            mean_data_l16 = ds16[sect].sel(z=z_sect).median("channel").data

            # create a mask from the scaled image
            # A- mask with similar l16 dimensions
            mask_image_l16_d = delayed(create_mask)(
                mean_data_l16,
                cl_morph_parm=10,
                c_min_area=0.0009,
                c_count_max=15,
                output_size=None,
            )

            mask_image_l16 = da.from_delayed(
                mask_image_l16_d, shape=mean_data_l16.shape, dtype="uint8"
            ).rechunk(mean_data_l16.chunksize)

            # B- mask with similar original data dimensions
            mask_image_d = delayed(create_mask)(
                mean_data_l16,
                cl_morph_parm=10,
                c_min_area=0.0009,
                c_count_max=15,
                output_size=mean_data_org.shape[::-1],
            )

            mask_image = da.from_delayed(
                mask_image_d, shape=mean_data_org.shape, dtype="uint8"
            ).rechunk(mean_data_org.chunksize)

            beads_df = bead_detect_worker(
                mean_data_org,
                mask_image,
                mean_data_l16,
                mask_image_l16,
                overlap_size=200,
            )
            beads_df["section"] = str(sect)
            beads_df["z"] = z_sect
            all_bead_z.append(beads_df)

            if fig:
                plot_beads(
                    mean_data_org,
                    mask_image,
                    beads_df,
                    fig_fname=output_path / "bead" / f"{sect}_z{z_sect}_bead.png",
                )
            # store the l16 and original-size mask in a npz and png file
            output_mask_png = output_path / "bead" / f"mask_{sect}_z{z_sect}.png"
            output_mask_npz = output_path / "bead" / f"mask_{sect}_z{z_sect}.npz"
            cv2.imwrite(str(output_mask_png), np.array(mask_image_l16) * 255)
            np.savez_compressed(str(output_mask_npz), np.array(mask_image))

            del mask_image
            del mean_data_org
            del mean_data_l16

        df = pd.concat(all_bead_z)
        df.to_parquet(output_bead)
        logger.info(
            "Bead detection done for section %s:Z%d (%d)", sect, z_sect, len(df)
        )

        trim_memory_workers()
        restart_workers()


# TODO: write as script
# if __name__ == "__main__":
