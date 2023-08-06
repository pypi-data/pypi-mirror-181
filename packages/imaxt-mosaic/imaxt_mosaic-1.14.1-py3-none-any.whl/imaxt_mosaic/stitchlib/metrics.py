from skimage.metrics import structural_similarity  # noqa: F401
from skimage.metrics import normalized_mutual_information, normalized_root_mse  # noqa: F401

from .mutual_information import mutual_information  # noqa: F401


def rmse(img1, img2):
    """Root Mean Squared Error"""
    res = normalized_root_mse(img1, img2)
    return 1 - res
