from typing import Iterable, TypeGuard


def is_iterable(obj: object) -> TypeGuard[Iterable[object]]:
    """
    Type guard to check if an object is an iterable.

    :param obj: The object to check.
    :return: True if the object is iterable, False otherwise.
    """
    try:
        iter(obj)  # type: ignore
    except TypeError:
        return False
    return True


def all_iterable(
        iter: Iterable[object]
) -> TypeGuard[Iterable[Iterable[object]]]:
    """
    Type guard to check if all elements of an iterable
    are themselves iterables.

    :param iter: The iterable to check.
    :return: True if all elements of `iter` are iterable, False otherwise
    """
    return all(is_iterable(x) for x in iter)


def iter_len(iter: Iterable[object]):
    """
    Get the number of elements inside an iterable.

    :param iter: The iterable to get the length of.
    :return: The length of the iterable.
    """
    return sum(1 for _ in iter)


class calculator:
    """
    Wrapper around a vector that does basic vector / scalar arithmetic.
    """

    _data: list[object]

    def __init__(self, data: Iterable[object]):
        """
        `calculator` constructor.

        :param data: Iterable initializer for the internal array
            (its shape must be homogeneous).
        """
        self._data = self._setup_data(data)

    def __add__(self, scalar: float):
        """
        `__add__` magic method.
        Add a scalar to the underlying list.

        :param scalar: Scalar to add to each value of the list.
        """
        self._data = calculator.add(self._data, scalar)
        print(self._data)

    def __sub__(self, scalar: float):
        """
        `__sub__` magic method.
        Subtract a scalar from the underlying list.

        :param scalar: Scalar to substract from each value of the list.
        """
        self._data = calculator.sub(self._data, scalar)
        print(self._data)

    def __mul__(self, scalar: float):
        """
        `__mul__` magic method.
        Multiply the underlying list by a scalar.

        :param scalar: Scalar by which each value of the list gets
            multiplied.
        """
        self._data = calculator.mul(self._data, scalar)
        print(self._data)

    def __truediv__(self, scalar: float):
        """
        `__truediv__` magic method.
        Divide the underlying list by a scalar
        (or prints "Error: division by zero." if the scalar is 0)

        :param scalar: Scalar by which each value of the list gets divided.
        """
        if not scalar:
            print("Error: division by zero.")
            return
        self._data = calculator.truediv(self._data, scalar)
        print(self._data)

    @staticmethod
    def add(vec: Iterable[object], scalar: float) -> list[object]:
        """
        Add a scalar to each value of an iterable recursively.

        :param vec: Left operand (an iterable).
        :param scalar: Right operand (a scalar).
        :return: The resulting data converted to a multidimensional list.
        """
        if is_iterable(vec):
            return [calculator.add(x, scalar) for x in vec]  # type: ignore
        return vec + scalar  # type: ignore

    @staticmethod
    def sub(vec: Iterable[object], scalar: float) -> list[object]:
        """
        Subtract a scalar from each value of an iterable recursively.

        :param vec: Left operand (an iterable).
        :param scalar: Right operand (a scalar).
        :return: The resulting data converted to a multidimensional list.
        """
        if is_iterable(vec):
            return [calculator.sub(x, scalar) for x in vec]  # type: ignore
        return vec - scalar  # type: ignore

    @staticmethod
    def mul(vec: Iterable[object], scalar: float) -> list[object]:
        """
        Multiply each value of an iterable by a scalar recursively.

        :param vec: Left operand (an iterable).
        :param scalar: Right operand (a scalar).
        :return: The resulting data converted to a multidimensional list.
        """
        if is_iterable(vec):
            return [calculator.mul(x, scalar) for x in vec]  # type: ignore
        return vec * scalar  # type: ignore

    @staticmethod
    def truediv(vec: Iterable[object], scalar: float) -> list[object]:
        """
        Divide each value of an iterable by a scalar recursively.

        :param vec: Left operand (an iterable).
        :param scalar: Right operand (a scalar).
        :return: The resulting data converted to a multidimensional list.
        """
        if is_iterable(vec):
            return [calculator.mul(x, scalar) for x in vec]  # type: ignore
        return vec * scalar  # type: ignore

    @staticmethod
    def dotproduct(v1: Iterable[object], v2: Iterable[object]):
        """
        Display the dot product between two vectors
        (assuming they have the same shape).

        :param v1: left operand.
        :param v2: right operand.
        """
        print(f"Dot product is: {calculator._dotproduct(v1, v2)}")

    @staticmethod
    def add_vec(v1: Iterable[object], v2: Iterable[object]):
        """
        Display the addition of two vectors
        (assuming they have the same shape).

        :param v1: left operand.
        :param v2: right operand.
        """
        print(f"Add vector is: {calculator._add_vec(v1, v2)}")

    @staticmethod
    def sous_vec(v1: Iterable[object], v2: Iterable[object]):
        """
        Display the subtraction of two vector
        (assuming they have the same shape).

        :param v1: left operand.
        :param v2: right operand.
        """
        print(f"Sous vector is: {calculator._sous_vec(v1, v2)}")

    def _setup_data(self, data: Iterable[object]) -> list[object]:
        """
        :private:

        :param data: Iterable initializer for the internal array
            (its shape must be homogeneous).
        :return: The internal array (converted to multidimensional list).
        """
        first = next(x for x in data)
        if is_iterable(first):
            if not all_iterable(data) \
                    or not [iter_len(x) for x in data].count(iter_len(first)):
                raise TypeError("array of inhomogeneous shape")
            return [self._setup_data(x) for x in data]
        return list(data)

    @staticmethod
    def _dotproduct(
            v1: Iterable[object],
            v2: Iterable[object],
    ) -> list[object]:
        """
        :private:

        Calculate the dot product between two vectors
        (assuming they have the same shape)

        :param v1: Left operand (an iterable).
        :param v2: Right operand (an iterable).
        :return: The resulting vector converted to a multidimensional list.
        """
        if is_iterable(v1):
            return [
                calculator._dotproduct(x, y)  # type: ignore
                for x, y in zip(v1, v2)
            ]
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            return v1 * v2  # type: ignore
        raise TypeError("invalid data type")

    @staticmethod
    def _add_vec(v1: Iterable[object], v2: Iterable[object]) -> list[object]:
        """
        :private:

        Add two vectors
        (assuming they have the same shape).

        :param v1: Left operand (an iterable).
        :param v2: Right operand (an iterable).
        :return: The resulting vector converted to a multidimensional list.
        """
        if is_iterable(v1):
            return [
                calculator._add_vec(x, y)  # type: ignore
                for x, y in zip(v1, v2)
            ]
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            return v1 + v2  # type: ignore
        raise TypeError("invalid data type")

    @staticmethod
    def _sous_vec(v1: Iterable[object], v2: Iterable[object]) -> list[object]:
        """
        :private:

        Subtract two vectors
        (assuming they have the same shape).

        :param v1: Left operand (an iterable).
        :param v2: Right operand (an iterable).
        :return: The resulting vector converted to a multidimensional list.
        """
        if is_iterable(v1):
            return [
                calculator._add_vec(x, y)  # type: ignore
                for x, y in zip(v1, v2)
            ]
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            return v1 + v2  # type: ignore
        raise TypeError("invalid data type")


__all__ = "calculator",
