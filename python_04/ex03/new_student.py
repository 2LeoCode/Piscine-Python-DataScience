import random
import string
from dataclasses import dataclass, field


def generate_id():
    return "".join(random.choices(string.ascii_lowercase, k=15))


@dataclass(slots=True)
class Student:
    """
    A student.

    :attr name: The student's name.
    :attr surname: The student's surname.
    :attr active: Whether the student is active or not.
    :attr login: The student's login.
    :attr id: The student's id.

    :constructor:
    :param name:
    :param surname:
    """
    name: str
    surname: str
    active: bool = field(init=False, default=True)
    login: str = field(init=False)
    id: str = field(init=False, default_factory=generate_id)

    def __post_init__(self):
        """
        `Student` post-constructor.

        Check if the name and surname are non-empty,
        and set the login attribute.
        """
        assert self.name and self.surname, "name and surname must be non-empty"
        self.login = self.name[0] + self.surname
