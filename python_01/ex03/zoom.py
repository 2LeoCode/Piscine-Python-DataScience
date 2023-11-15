from load_image import ft_load
from matplotlib import pyplot as plt
import numpy as np


def zoom():
    """
    Apply a custom zoom on the image "animal.jpeg" and display it.
    """
    try:
        img = ft_load("animal.jpeg")
    except Exception as e:
        print(e)
        return
    zoomed = np.asarray(
        img[100:500, 450:850][..., :3].dot(
            (0.2989, 0.5870, 0.1140)
        )[..., np.newaxis],
        dtype=np.uint8
    )
    print(
        f"{img}\n"
        f"New shape after slicing: {zoomed.shape}\n"
        f"{zoomed}"
    )
    plt.imshow(zoomed, cmap="gray")
    plt.show()
    np.save("animal_zoomed.npy", zoomed)


if __name__ == "__main__":
    zoom()

__all__ = "zoom",
