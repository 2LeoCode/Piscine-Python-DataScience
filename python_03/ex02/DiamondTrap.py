from S1E7 import Baratheon, Lannister
from typing_extensions import override


class King(Baratheon, Lannister):
    """
    Character that is a King, it belongs to both `Baratheon` and
    `Lannister` families.
    """

    @override
    def __init__(self, first_name: str, is_alive: bool = True):
        super().__init__(first_name, is_alive)
        self.family_name = "Baratheon"


__all__ = "King",
