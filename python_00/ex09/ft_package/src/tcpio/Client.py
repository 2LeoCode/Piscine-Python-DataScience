from dataclasses import dataclass
from typing import TypeAlias, Final
from typing_extensions import override
from select import poll, POLLIN, POLLOUT, POLLERR
from socket import socket, AF_INET, SOCK_STREAM, SOCK_NONBLOCK, IPPROTO_TCP, \
    getaddrinfo, AddressFamily, SocketKind
from time import sleep, time
from .SocketIO import SocketIO
from signal import signal, SIGINT
from types import FrameType
import atexit

AddressInfo: TypeAlias = list[tuple[
    AddressFamily,
    SocketKind,
    int,
    str,
    tuple[str, int] | tuple[str, int, int, int],
]]


@dataclass(slots=True, init=False)
class Client(SocketIO):
    """
    A client that connects to a `tcpio.Server`.

    :attr host: The client's host name.
    :attr port: The client's port number.
    :attr connected: Whether the client is connected to the server.
    :attr special_events: Special events that are triggered by the client.

    List of special events:
        - `connect` -> The client is successfully connected to the server, the
            callback takes no arguments.
        - `disconnection` -> The client is disconnected from the server, the
            callback takes no arguments.
        - `error` -> Triggered when an error occurs, the callback takes
            an `Exception` as its first argument.
    """
    host: Final[str]
    port: Final[str]
    connect_timeout: Final[float]
    reconnection: Final[bool]
    reconnection_attempts: Final[int]
    reconnection_delay: Final[float]
    reconnection_delay_max: Final[float]

    _connected: bool
    _poller: poll
    _addr_info: AddressInfo
    _first_conn: bool

    @override
    def __init__(
            self,
            address: str,
            connect_timeout: float = 1,
            reconnection: bool = True,
            reconnection_attempts: int = 0,
            reconnection_delay: float = 0.5,
            reconnection_delay_max: float = 5,
            handle_sigint: bool = True,
            buffer_size: int = 4096,
    ):
        """
        `tcpio.Client` constructor.

        :param address: The address of the server to connect to.
        :param connect_timeout: The timeout for the connection.
        :param reconnection: Whether to attempt to reconnect to the server.
        :param reconnection_attempts: The number of reconnection attempts
            (0 = infinite).
        :param reconnection_delay: The first delay between reconnection
            attempts (doubled on each retry).
        :param reconnection_delay_max: The maximum delay between reconnection
            attempts.
        :param handle_sigint: Whether to handle SIGINT (Ctrl+C).
        """
        if handle_sigint:
            def sigint_handler(sig: int, frame: FrameType | None):
                self.disconnect()
            signal(SIGINT, sigint_handler)
        port_sep = address.rfind(":")
        self.host = address[:port_sep]
        self.port = address[port_sep + 1:]
        super(Client, self).__init__(
            socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, IPPROTO_TCP),
            buffer_size,
        )
        self.connect_timeout = connect_timeout
        self.reconnection = reconnection
        self.reconnection_attempts = reconnection_attempts
        self.reconnection_delay = reconnection_delay
        self.reconnection_delay_max = reconnection_delay_max
        self._poller = poll()
        self._connected = False
        self._addr_info = getaddrinfo(
            host=self.host,
            port=self.port,
            family=AF_INET,
            type=SOCK_STREAM,
            proto=IPPROTO_TCP,
        )
        self._first_conn = True
        self._poller.register(self._socket.fileno())
        atexit.register(self._atexit)

    def wait(self):
        """
        Wait for the client to disconnect.
        """
        while self._connected:
            self.sleep()

    def _atexit(self):
        """
        Executes automatically when the program exits.
        Wait for the client to disconnect before it gets out of scope,
        then trigger the `disconnect` events before closing the socket.
        """
        if self._first_conn:
            self.connect()
        if self._connected:
            self.wait()
            self._trigger_event("disconnect")
            if self._connected:
                # case where user reconnects in disconnect handler
                self._atexit()
        self._socket.close()

    @property
    def connected(self):
        """
        `connected` getter.

        :return: Whether the client is connected to the server.
        """
        return self._connected

    @property
    def special_events(self):
        """
        `special_events` getter.

        :return: Special events that are triggered by the client.
        """
        return "connect", "disconnect", "error"

    def disconnect(self):
        """
        Disconnect the client from the server.
        """
        self._connected = False

    def sleep(self, seconds: float = 0):
        """
        Sleep for `seconds` seconds, if `seconds` is 0, sleep until the next
        event is triggered.

        :param seconds: The number of seconds to sleep.
        """
        begin = time()
        while True:
            if fd_events := self._poller.poll():
                _, events = fd_events[0]
                if events & POLLIN:
                    if not self._recv():
                        self._connected = False
                        break
                if events & POLLOUT:
                    self._send()
                if time() - begin > seconds:
                    break

    def connect(self):
        """
        Connect the client to the server.
        If `reconnection` was set to `True` in the constructor, attempt to
        reconnect to the server if the connection fails.
        Trigger the `error` events on each failed attempt with a
        `ConnectionError` as their first argument.
        When the connection is successful, trigger the `connect` event.
        """
        reconnect_interval = self.reconnection_delay
        attempts = 1
        if not self._first_conn:
            self._poller.unregister(self._socket.fileno())
            self._socket = socket(
                family=AF_INET,
                type=SOCK_STREAM | SOCK_NONBLOCK,
                proto=IPPROTO_TCP,
            )
            self._poller.register(self._socket.fileno())
        while not self._connected and (
            self.reconnection and (
                not self.reconnection_attempts or
                attempts <= self.reconnection_attempts
            )
        ):
            if reconnect_interval > self.reconnection_delay_max:
                reconnect_interval = self.reconnection_delay_max
            self._poller.modify(self._socket.fileno(), POLLOUT)
            for addr_info in self._addr_info:
                try:
                    self._socket.connect(addr_info[-1])
                except BlockingIOError:
                    fd_events = self._poller.poll(self.connect_timeout * 1000)
                    _, event = fd_events[0]
                    if event & POLLOUT and not event & POLLERR:
                        self._connected = True
                except Exception:
                    pass
                else:
                    self._connected = True
                finally:
                    if self._connected:
                        break
            if not self._connected:
                self._trigger_event("error", ConnectionError)
                sleep(reconnect_interval)
                attempts += 1
                reconnect_interval *= 2
        self._trigger_event("connect")
        self._poller.modify(self._socket, POLLIN | POLLOUT)
        self._first_conn = False


__all__ = "Client", "AddressInfo"
