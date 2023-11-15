from S1E9 import Character
from typing_extensions import override


class Baratheon(Character):
    """
    Character that belongs to the Baratheon family.
    """

    @override
    def attack(self, other: Character):
        print(f"{self.first_name}: Ours is the fury!")
        other.die()


class Lannister(Character):
    """
    Character that belongs to the Lannister family.
    """

    @classmethod
    def create_lannister(cls, first_name: str, is_alive: bool):
        """
        Alias to `Lannister.create_character`.
        """
        return cls.create_character(first_name, is_alive)

    @override
    def attack(self, other: Character):
        print(f"{self.first_name}: Hear me roar!")
        other.die()


__all__ = "Lannister", "Baratheon"
