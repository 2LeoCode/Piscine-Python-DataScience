from typing import \
    Callable, TypeGuard, TypeVar, Generic, Any, overload, \
    Generator
from collections.abc import Iterator, Iterable
from typing_extensions import Self

T = TypeVar("T")
U = TypeVar("U")


class ft_filter(Iterator[T], Generic[T]):
    """
    Reimplementation of the builtin filter class.
    """
    _stream: Generator[T, None, None]

    @overload
    def __new__(cls, __function: None, __iterable: Iterable[T | None]) -> Self:
        """
        Remove all None values from `__iterable`.

        :param __function: `None`.
        :param __iterable: an iterable of `T | None`.
        """
        ...

    @overload
    def __new__(
        cls, __function: Callable[[U], TypeGuard[T]], __iterable: Iterable[U]
    ) -> Self:
        """
        Remove all values from `__iterable` that are not of type `T`.
        The type of the values is checked with `__function`.

        :param __function: a type guard function.
        :param __iterable: an iterable of any type.
        """
        ...

    @overload
    def __new__(
        cls, __function: Callable[[T], Any], __iterable: Iterable[T]
    ) -> Self:
        """
        Remove all values from `__iterable` for which the predicate
        function `__function` returns a falsy value.

        :param __function: a predicate function.
        :param __iterable: an iterable of `T`.
        """
        ...

    def __new__(cls, *args: Any):
        instance = super().__new__(cls)
        instance._stream = (
            x for x in args[1] if (x if args[0] is None else args[0](x))
        )
        return instance

    def __next__(self) -> T:
        return next(self._stream)


__all__ = "ft_filter",
