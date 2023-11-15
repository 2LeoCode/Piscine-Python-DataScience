from .Event import Event
from dataclasses import dataclass, field
from typing import TypeVar, ParamSpec, Callable, Any, overload, Final
from abc import ABC, abstractmethod

RT = TypeVar('RT')
P = ParamSpec('P')


@dataclass(slots=True)
class IO(ABC):
    """
    Base class for event-based I/O.
    """
    _events: Final[dict[str, list[Event]]] = field(
        init=False,
        default_factory=dict,
    )

    @abstractmethod
    def emit(self, event: str, *args: object, **kwargs: object) -> None:
        """
        Emit the event `event` with `args` and `kwargs` as arguments.

        :param event: The event to emit.
        :param args: The arguments to pass to the event's callbacks.
        :param kwargs: The keyword arguments to pass to the event's callbacks.
        """
        ...

    @overload
    def on(self, __callback: Callable[P, RT]) -> Callable[P, RT]:
        """
        Add a new event listener on the event `__callback.__name__`.

        :param __callback: The event listener to add.
        :return: `__callback`.
        """
        ...

    @overload
    def on(self, __event: str, __callback: Callable[P, RT]) -> Callable[P, RT]:
        """
        Add a new event listener on the event `__event`.

        :param __event: The event to listen to.
        :param __callback: The event listener to add.
        :return: `__callback`.
        """
        ...

    def on(self, *args: Any):
        if len(args) == 1:
            return self.on(args[0].__name__, args[0])
        event, callback = args
        self._events[event] = [*self._events.get(event, []), callback]
        return callback

    @overload
    def once(self, __callback: Callable[P, RT]) -> Callable[P, RT]:
        """
        Add a new one-time event listener on the event `__callback.__name__`.

        :param __callback: The event listener to add.
        :return: `__callback`.
        """
        ...

    @overload
    def once(
            self,
            __event: str,
            __callback: Callable[P, RT]
    ) -> Callable[P, RT]:
        """
        Add a new one-time event listener on the event `__event`.

        :param __event: The event to listen to.
        :param __callback: The event listener to add.
        :return: `__callback`.
        """
        ...

    def once(self, *args: Any):
        if len(args) == 1:
            return self.once(args[0].__name__, args[0])
        event, callback = args

        def wrapper(*args: Any, **kwargs: Any) -> None:
            self.off(wrapper)
            callback(*args, **kwargs)
        return self.on(event, wrapper)

    @overload
    def off(self, __callback: Callable[..., object]) -> None:
        """
        Remove the event listener `__callback` from the internal events map.

        :param __callback: The event listener to remove.
        """
        ...

    @overload
    def off(self, __event: str, __callback: Callable[..., object]) -> None:
        """
        Remove the event listener `__callback` from the internal events map
        at the `__event` entry.

        :param __event: The event to remove the event listener from.
        :param __callback: The event listener to remove.
        """
        ...

    @overload
    def off(self, __event: str) -> None:
        """
        Remove all the event listeners from the internal events map at the
        `__event` entry.

        :param __event: The event to remove the event listeners from.
        """
        ...

    @overload
    def off(self) -> None:
        """
        Clear the internal events map.
        """
        ...

    def off(self, *args: Any):
        if not args:
            self._events.clear()
        elif len(args) == 1:
            if isinstance(args[0], str):
                self._events.pop(args[0], None)
            else:
                for name, events in self._events.items():
                    if args[0] in events:
                        return self.off(name, args[0])
        else:
            self._events[args[0]].remove(args[1])

    def _trigger_event(self, event: str, *args: object, **kwargs: object):
        """
        :private:

        Execute all event listeners bound to `event`.

        :param event: The event to trigger.
        :param args: The arguments to pass to the event's callbacks.
        :param kwargs: The keyword arguments to pass to the event's callbacks.
        """
        for callback in self._events.get(event, []):
            callback(*args, **kwargs)
