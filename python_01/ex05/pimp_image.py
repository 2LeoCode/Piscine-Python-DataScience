from numpy._typing import _ArrayLike
import numpy as np


def ft_invert(array: _ArrayLike[np.uint8]):
    """
    Invert the color of a given image in RGB format.

    :param array: a numpy array of shape (height, width, 3) and dtype uint8.
    """
    return np.asarray(255 - np.asarray(
        array, dtype=np.uint8
    ), dtype=np.uint8)


def ft_red(array: _ArrayLike[np.uint8]):
    """
    Apply a red filter to a given image in RGB format.

    :param array: a numpy array of shape (height, width, 3) and dtype uint8.
    """
    array = np.asarray(array)
    new_array = np.zeros_like(array)
    new_array[:, :, 0] = array[:, :, 0]
    return new_array


def ft_green(array: _ArrayLike[np.uint8]):
    """
    Apply a green filter to a given image in RGB format.

    :param array: a numpy array of shape (height, width, 3) and dtype uint8.
    """
    array = np.asarray(array)
    new_array = np.zeros_like(array)
    new_array[:, :, 1] = array[:, :, 1]
    return new_array


def ft_blue(array: _ArrayLike[np.uint8]):
    """
    Apply a blue filter to a given image in RGB format

    :param array: a numpy array of shape (height, width, 3) and dtype uint8.
    """
    array = np.asarray(array)
    new_array = np.zeros_like(array)
    new_array[:, :, 2] = array[:, :, 2]
    return new_array


def ft_grey(array: _ArrayLike[np.uint8]):
    """
    Apply a grey filter to a given image in RGB format.

    :param array: a numpy array of shape (height, width, 3) and dtype uint8.
    """
    return np.asarray(np.dot(array, (0.2989, 0.5870, 0.1140)), dtype=np.uint8)


__all__ = "ft_invert", "ft_red", "ft_green", "ft_blue", "ft_grey"
