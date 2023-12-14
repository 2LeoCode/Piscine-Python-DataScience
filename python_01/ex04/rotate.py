from typing import TypeVar
from numpy._typing import _ArrayLike
from matplotlib import pyplot as plt
from zoom import zoom
from load_image import ft_load
import numpy as np

T = TypeVar("T", bound=np.generic, covariant=True)


def transpose(data: _ArrayLike[T], axes: tuple[int, ...] | None = None):
    """
    Transpose a given array according to the given axes.

    :param data: a numpy array.
    :param axes: a tuple of ints representing the new axes order.
    """
    data = np.asarray(data)
    shape = data.shape
    if axes is None:
        axes = tuple(range(len(shape)))[::-1]

    if len(axes) != len(shape):
        raise ValueError("axes don't match array")
    if set(axes) != set(range(len(shape))):
        raise ValueError("axes don't match array")
    transposed_shape = tuple(shape[i] for i in axes)
    print(f"New shape after rotation: {transposed_shape}")
    transposed = np.zeros(transposed_shape, dtype=data.dtype)
    for idx in np.ndindex(shape):
        transposed_idx = tuple(idx[i] for i in axes)
        transposed[transposed_idx] = data[idx]
    return transposed


def start():
    """
    Rotate the image "animal_zoomed" 90 degrees and display it
    """
    try:
        img = zoom(ft_load("animal.jpeg"))
    except Exception as e:
        f"{type(e).__name__}: {e}"
        exit(1)
    print(f"The shape of the image is {img.shape}\n{img}")
    rotated = transpose(img, (1, 0, 2)).squeeze(axis=2)
    print(rotated)
    plt.imshow(rotated, cmap="gray")
    plt.show()


if __name__ == "__main__":
    start()

__all__ = "rotate",
