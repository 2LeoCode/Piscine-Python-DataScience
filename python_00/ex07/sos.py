import sys


class NestedMorse:
    TABLE = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----",
        " ": "/",
    }


def sos(text: str):
    """
    Display the morse code of the given text.

    :param text: a string containing only alphanumeric characters.
    """
    print(" ".join(NestedMorse.TABLE[c] for c in text.upper()))


if __name__ == "__main__":
    assert len(sys.argv) == 2 \
        and all(c in NestedMorse.TABLE for c in sys.argv[1].upper()), \
        "Usage: python3 sos.py <a-zA-Z0-9 text>"
    sos(sys.argv[1])

__all__ = "sos",
