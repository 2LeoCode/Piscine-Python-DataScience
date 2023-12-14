import numpy as np
from matplotlib import image as img


def ft_load(path: str):
    """
    Load an image from a given path, print its shape
    and return it as a numpy array of RGB pixels.

    :param path: the path to the image.
    """
    data = img.imread(path).astype(np.uint8)
    print(f"The shape of the image is: {data.shape}")
    return data


__all__ = "ft_load",
