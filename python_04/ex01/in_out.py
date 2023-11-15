from typing import Callable


def square(x: float):
    """
    Get the square of a number.

    :param x: The number to square.
    :return: The square of the number.
    """
    return x ** 2


def pow(x: float):
    """
    Power a number to himself.

    :param x: The number to power to himself.
    :return: The number powered to himself.
    """
    return x ** x


def outer(x: float, function: Callable[[float], float]):
    """
    Return a function that applies a function to a number,
    updating the number each time.

    :param x: The initial value of the number to apply the function to.
    :param function: The function to apply to the number.
    :return: A function that applies `function` to a number,
        updating the number each time.
    """
    def inner():
        """
        Update the non local variable `x` with `function` and return it.

        :return: The updated value of `x`.
        """
        nonlocal x
        x = function(x)
        return x
    return inner


__all__ = "square", "pow", "outer"
