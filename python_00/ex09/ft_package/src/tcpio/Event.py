from typing import Protocol


class Event(Protocol):
    """
    Type hint for event callbacks.
    """
    def __call__(self, *args: object, **kwargs: object) -> None:
        ...
