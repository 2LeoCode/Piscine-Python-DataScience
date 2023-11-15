from ft_filter import ft_filter
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


def filterstring(text: str, max_word_size: int):
    """
    Display the words of the text that are longer than
    or equal to the given size.

    :param text: a string.
    :param max_word_size: the minimum size of the words to display.
    """
    print(list(ft_filter(
        lambda word: len(word) >= max_word_size, text.split(" ")
    )))


if __name__ == "__main__":
    assert len(sys.argv) == 3 and convertible_to(sys.argv[2], int), \
        "Usage: python3 filterstring.py <text> <max_word_size>"
    filterstring(sys.argv[1], int(sys.argv[2]) + 1)

__all__ = "filterstring",
