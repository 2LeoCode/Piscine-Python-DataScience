from abc import ABC, abstractmethod
from typing_extensions import override


class Character(ABC):
    """
    Character interface.

    :attr first_name: the first name of the character.
    :attr is_alive: a boolean that indicates if the character is alive.
    """

    first_name: str
    is_alive: bool

    def __init__(self, first_name: str, is_alive: bool = True):
        """
        `Character` constructor.

        :param first_name: the first name of the character.
        :param is_alive: a boolean that indicates if the character is alive.
        """
        self.__dict__ |= {
            "first_name": first_name,
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


class Stark(Character):
    """
    Character that belongs to the Stark family.
    """

    @override
    def attack(self, other: Character):
        print(f"{self.first_name}: Winter is coming!")
        other.die()


__all__ = "Character", "Stark"
