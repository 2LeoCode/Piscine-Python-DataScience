import numpy as np
from pimp_image import \
                    ft_invert, \
                    ft_red, \
                    ft_green, \
                    ft_blue, \
                    ft_grey
from typing import cast
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import load_image as img

array = np.asarray(img.ft_load("landscape.jpg"), dtype=np.uint8)
print(array)

_, axs = plt.subplots(2, 3)
axs_list = cast(list[Axes], axs.flatten().tolist())

axs_list[0].imshow(array)
axs_list[1].imshow(ft_invert(array))
axs_list[2].imshow(ft_red(array))
axs_list[3].imshow(ft_green(array))
axs_list[4].imshow(ft_blue(array))
axs_list[5].imshow(ft_grey(array), cmap="gray")

plt.show()
help(ft_invert)
