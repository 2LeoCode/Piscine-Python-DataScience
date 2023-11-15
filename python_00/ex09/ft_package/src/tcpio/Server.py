from typing import TypeAlias, Final
from typing_extensions import override
from select import poll, POLLIN, POLLOUT
from dataclasses import dataclass, field, InitVar
from .IO import IO
from .SocketIO import SocketIO
from socket import socket, getaddrinfo, AF_INET, SOCK_STREAM, \
    IPPROTO_TCP, AddressFamily, SocketKind, error as SocketError, \
    SOCK_NONBLOCK
from time import time
from signal import signal, SIGINT
from types import FrameType
import sys
import atexit

AddressInfo: TypeAlias = list[tuple[
    AddressFamily,
    SocketKind,
    int,
    str,
    tuple[str, int] | tuple[str, int, int, int],
]]


@dataclass(slots=True)
class Server(IO):
    """
    An event-based TCP server.

    :attr socket: The server's internal socket.
    :attr clients: The list of connected clients.
    :attr host: The server's host name.
    :attr port: The server's port number.
    :attr special_events: Special events that are triggered by the server.

    List of special events:
        - `connection` -> A client connects to the server, the callback takes
            a `tcpio.Server.Client` as its first argument.
        - `disconnection` -> A client disconnects from the server, the callback
            takes a `tcpio.Server.Client` as its first argument.
        - `error` -> Triggered when an error occurs, the callback takes
            an `Exception` as its first argument.
    """
    @dataclass(slots=True, init=False)
    class Client(SocketIO):
        """
        A client connected to a `tcpio.Server`.

        :attr addr: The client's address.
        :attr socket: The client's internal socket.
        """
        addr: Final[object]
        _server: Final["Server"]

        @override
        def __init__(
                self,
                socket: socket,
                addr: object,
                server: "Server",
                buffer_size: int = 4096,
        ):
            """
            `tcpio.Server.Client` constructor.

            :param socket: The client's internal socket.
            :param addr: The client's address.
            :param server: The server that the client is connected to.
            :param buffer_size: The size of the client's internal buffer.
            """
            super(Server.Client, self).__init__(socket, buffer_size)
            self.addr = addr
            self._server = server

        def __del__(self):
            self._socket.close()

        @override
        def _trigger_event(self, event: str, *args: object, **kwargs: object):
            self._server._trigger_event(event, self, *args, **kwargs)
            super(Server.Client, self)._trigger_event(event, *args, **kwargs)

        def disconnect(self, trigger_disconnection: bool = True):
            """
            Call `self._server.disconnect(self, trigger_disconnection)`.

            :param trigger_disconnection: Whether or not to trigger the
                `disconnection` events on the server.
            """
            self._server.disconnect(self, trigger_disconnection)

    _socket: socket = field(init=False)
    _clients: list[Client] = field(init=False, default_factory=list)
    _poller: poll = field(init=False, default_factory=poll)
    _stopped: bool = field(init=False, default=False)
    _addr_info: AddressInfo = field(init=False)
    _host: str = field(init=False)
    _port: str = field(init=False)
    _bound: bool = field(init=False, default=False)
    _first_start: bool = field(init=False, default=True)

    address: InitVar[str] = "localhost:3000"
    handle_sigint: InitVar[bool] = True

    def __post_init__(self, address: str, handle_sigint: bool):
        """
        `tcpio.Server` post constructor.

        :param address: The address to bind the server to.
        :param handle_sigint: Whether or not to handle SIGINT (Ctrl+C).
        """
        if handle_sigint:
            def sigint_handler(sig: int, frame: FrameType | None):
                self.stop()
            signal(SIGINT, sigint_handler)
        port_sep = address.rfind(":")
        self._host = address[:port_sep]
        self._port = address[port_sep+1:]
        self._socket = socket(
            AF_INET, SOCK_STREAM | SOCK_NONBLOCK, IPPROTO_TCP)
        self._addr_info = getaddrinfo(
            host=self._host,
            port=self._port,
            family=AF_INET,
            type=SOCK_STREAM,
            proto=IPPROTO_TCP,
        )

    @override
    def emit(self, event: str, *args: object, **kwargs: object):
        """
        Emit an event to all the clients connected to the server.

        :param event: The event to emit.
        :param args: The arguments to pass to the event's callbacks.
        :param kwargs: The keyword arguments to pass to the event's callbacks.
        """
        for client in self.clients:
            client.emit(event, *args, **kwargs)

    def _atexit(self):
        """
        Executes automatically before the program exits.
        Wait for the server to be stopped and disconnect all the clients.
        """
        self.wait()
        for client in self._clients:
            client.disconnect()
        self._clients.clear()
        self._socket.close()

    @property
    def socket(self):
        """
        `socket` getter.

        :return: The server's internal socket.
        """
        return self._socket

    @property
    def clients(self):
        """
        `clients` getter.

        :return: A copy of the server's connected clients.
        """
        return list(self._clients)

    @property
    def host(self):
        """
        `host` getter.

        :return: The server's host name.
        """
        return self._host

    @property
    def port(self):
        """
        `port` getter.

        :return: The server's port number.
        """
        return self._port

    @property
    def special_events(self):
        """
        `special_events` getter.

        :return: The server's special event names.
        """
        return "connection", "disconnection", "error"

    def stop(self):
        """
        Stop the server.
        """
        self._stopped = True

    def disconnect(self, client: Client, trigger_disconnection: bool = True):
        """
        Disconnect the client from the server, if `trigger_disconnection` is
        `True`, the `disconnection` events will be triggered before the
        client gets disconnected.

        :param client: The client to disconnect.
        :param trigger_disconnection: Whether or not to trigger the
            `disconnection` events on the server.
        """
        if trigger_disconnection:
            self._trigger_event("disconnection", client)
        self._poller.unregister(client._socket.fileno())
        client._socket.setblocking(True)
        client._socket.send(
            client._send_buffer + (0).to_bytes(8, sys.byteorder)
        )
        self._clients.remove(client)

    def wait(self):
        """
        Wait for the server to be stopped.
        """
        while not self._stopped:
            self.sleep()

    def sleep(self, seconds: float = 0):
        """
        Sleep for `seconds` seconds or until the server gets stopped,
        while sleeping, process the incoming and outgoing data of the
        connected clients.

        :param seconds: The number of seconds to sleep.
        """
        begin = time()
        while not self._stopped:
            for fd, event in self._poller.poll(0):
                if fd == self._socket.fileno():
                    incoming, addr = self._socket.accept()
                    incoming.setblocking(False)
                    self._clients.append(
                        Server.Client(
                            socket=incoming,
                            addr=addr,
                            server=self,
                        )
                    )
                    self._trigger_event("connection", self.clients[-1])
                    self._poller.register(incoming, POLLIN | POLLOUT)
                else:
                    client = next(
                        client for client in self.clients
                        if client._socket.fileno() == fd
                    )
                    if event & POLLIN:
                        if client._recv() is False:
                            self._poller.unregister(fd)
                            self._trigger_event("disconnection", client)
                            self._clients.remove(client)
                    if event & POLLOUT:
                        client._send()

            if time() - begin > seconds:
                break

    def start(self, block: bool = False):
        """
        Start the server, if `block` is `True`, the `wait` method will be
        called just before returning.

        :param block: Whether or not to block until the server is stopped.
        """
        if self._bound:
            raise RuntimeError("Server already started")
        if not self._bound:
            for addr in self._addr_info:
                try:
                    self._socket.bind(addr[4])
                except SocketError:
                    continue
                else:
                    self._bound = True
                    break
            if not self._bound:
                self._trigger_event("error", "failed to bind")
                return
            atexit.register(self._atexit)
            self._socket.listen(128)
            self._poller.register(self._socket, POLLIN)
        self._stopped = False
        if block:
            self.wait()
