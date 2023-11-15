from string import punctuation
from dataclasses import dataclass
import sys


@dataclass(slots=True, init=False)
class StringInfo:
    """
    Class used to store information about a string.

    :attr length: the length of the string.
    :attr upper: the number of upper case letters.
    :attr lower: the number of lower case letters.
    :attr punct: the number of punctuation marks.
    :attr space: the number of spaces.
    :attr digit: the number of digits.
    """

    length: int
    upper: int
    lower: int
    punct: int
    space: int
    digit: int

    def __init__(self, text: str):
        """
        `StringInfo` constructor.

        :param text: a string to get information from.
        """
        self.length = len(text)
        self.upper = sum(1 for c in text if c.isupper())
        self.lower = sum(1 for c in text if c.islower())
        self.punct = sum(1 for c in text if c in punctuation)
        self.space = sum(1 for c in text if c.isspace())
        self.digit = sum(1 for c in text if c.isdigit())

    def __str__(self):
        """
        `StringInfo` string representation.
        """
        return \
            f"The text contains {self.length} characters:\n" \
            f"{self.upper} upper letters\n" \
            f"{self.lower} lower letters\n" \
            f"{self.punct} punctuation marks\n" \
            f"{self.space} spaces\n" \
            f"{self.digit} digits"


def building(text: str):
    """
    Display the following:
        - The length of the string
        - The number of upper case letters
        - The number of lower case letters
        - The number of punctuation marks
        - The number of spaces
        - The number of digits

    :param text: a string to get information from.
    """
    print(StringInfo(text))


if __name__ == "__main__":
    building(input() if len(sys.argv) < 2 else " ".join(sys.argv[1:]))

__all__ = "building",
