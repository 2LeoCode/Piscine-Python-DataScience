from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Message:
    """
    This class represents the kind of data that is sent between the client
    and the server.

    :attr event: The event that the message is associated with.
    :attr args: The arguments of the event.
    :attr kwargs: The keyword arguments of the event.
    """
    event: str
    args: tuple[object, ...]
    kwargs: dict[str, object]
