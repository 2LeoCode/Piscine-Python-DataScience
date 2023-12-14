from load_image import ft_load
from matplotlib import pyplot as plt
from numpy.typing import NDArray
import numpy as np


def zoom(img: NDArray[np.uint8]):
    """
    Apply a custom zoom on the image "animal.jpeg" and display it.
    """
    return np.asarray(
        img[100:500, 450:850][..., :3].dot(
            (0.2989, 0.5870, 0.1140)
        )[..., np.newaxis],
        dtype=np.uint8
    )


def start():
    try:
        img = ft_load("animal.jpeg")
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        exit(1)
    print(img)
    img = zoom(img)
    print(f"New shape after slicing: {img.shape}\n{img}")
    plt.imshow(img, cmap="grey")
    plt.show()


if __name__ == "__main__":
    start()

__all__ = "zoom",
