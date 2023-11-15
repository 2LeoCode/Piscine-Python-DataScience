from typing import TypeVar
from collections.abc import Sequence

T = TypeVar("T", bound=Sequence[object], covariant=True)


def slice_me(family: list[T], start: int, end: int):
    """
    Return a slice of the given list.

    :param family: a list of any python objects.
    :param start: the start of the slice.
    :param end: the end of the slice.
    :return: a slice of the given list.
    """
    if (
        not isinstance(family, list)
        or not all(isinstance(x, list) for x in family)
        or (len(family) and not all(len(x) == len(family[0]) for x in family))
    ):
        raise TypeError("family must be a two-dimensional array like list")
    slice = family[start:end]
    if not family:
        print("My shape is: (0, 0)\nMy new shape is: (0, 0)")
    else:
        old_shape = len(family), len(family[0])
        new_shape = len(slice), len(slice[0])
        print(f"My shape is: {old_shape}\nMy new shape is: {new_shape}")
    return slice


__all__ = "slice_me",
