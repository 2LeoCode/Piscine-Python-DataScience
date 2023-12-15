from abc import ABC, abstractmethod
from typing_extensions import override


class Character(ABC):
    """
    Character interface.

    :attr first_name: the first name of the character.
    :attr is_alive: a boolean that indicates if the character is alive.
    """

    first_name: str
    family_name: str
    is_alive: bool

    def __init__(self, first_name: str, is_alive: bool = True):
        """
        `Character` constructor.

        :param first_name: the first name of the character.
        :param is_alive: a boolean that indicates if the character is alive.
        """
        self.__dict__ |= {
            "first_name": first_name,
            "family_name": self.__class__.__name__,
            "is_alive": is_alive,
        }

    @abstractmethod
    def attack(self, other: "Character"):
        """
        Attack another character.

        :param other: the character to attack.
        """
        ...

    def die(self):
        """
        Die (set self.is_alive to False).
        """
        self.is_alive = False

    @classmethod
    def create_character(cls, first_name: str, is_alive: bool = True):
        """
        Factory method to create characters in a chain.

        :param first_name: The first name of the character.
        :param is_alive: A boolean to indicate if the character is alive.
        """
        return cls(first_name, is_alive)

    def __str__(self):
        """
        `__str__` magic method of `Character`.

        :return: A string representation of the `Character` instance.
        """
        return f"Character {self.first_name} {self.family_name} " \
            f"({'alive' if self.is_alive else 'dead'})"

    def __repr__(self):
        """
        `__repr__` magic method of `Character`.

        :return: A python-interpretable string representation of the
            `Character` instance.
        """
        return f"{self.family_name}({self.first_name}, {self.is_alive})"


class Stark(Character):
    """
    Character that belongs to the Stark family.
    """

    @override
    def attack(self, other: Character):
        print(f"{self.first_name}: Winter is coming!")
        other.die()


__all__ = "Character", "Stark"
