import sys


def convertible_to(object: object, type: type):
    """
    Return True if the object can be converted to the
    given type, otherwise return False.

    :param object: any python object.
    :param type: a python type.
    :return: True if the object can be converted to the
        given type, otherwise False.
    """
    try:
        type(object)
    except ValueError:
        return False
    return True


def whatis(number: int):
    """
    Display `I'm odd` if the integer given as argument is odd,
    otherwise display `I'm even`.

    :param number: an integer.
    """
    print("I'm odd" if number % 2 else "I'm even")


if __name__ == "__main__":
    assert len(sys.argv) == 2 and convertible_to(sys.argv[1], int), \
        f"Usage: {sys.executable} whatis.py <integer>"
    whatis(int(sys.argv[1]))

__all__ = "whatis",
