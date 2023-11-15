from typing import Callable, ParamSpec, TypeVar
import functools as ft

P = ParamSpec("P")
R = TypeVar("R")


def callLimit(limit: int):
    """
    Generate a decorator that limits the number of calls to a function.

    :param limit: The maximum number of calls to the function.
    :return: The decorator.
    """
    def callLimiter(function: Callable[P, R]) -> Callable[P, R | None]:
        """
        Decorator that limits the number of calls to a function.

        :param function: The function to limit the number of calls of.
        :return: The decorated function.
        """
        @ft.wraps(function)
        def limit_function(*args: P.args, **kwargs: P.kwargs) -> R | None:
            nonlocal limit
            if limit:
                limit -= 1
                return function(*args, **kwargs)
            print(f"Error: {function} call too many times.")
        return limit_function
    return callLimiter


__all__ = "callLimit",
