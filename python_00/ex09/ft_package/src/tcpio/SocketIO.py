from dataclasses import dataclass, field
from .IO import IO
from .Message import Message
from socket import socket
import pickle as pkl
import sys as sys
from typing import cast, Final
from typing_extensions import override


@dataclass(slots=True)
class SocketIO(IO):
    """
    Base class for a buffered socket I/O.

    :attr socket: The socket to use.
    :attr buffer_size: The size of the read buffer.
    """
    _socket: socket
    buffer_size: Final[int] = 4096

    _recv_buffer: bytes = field(init=False, default=b'')
    _send_buffer: bytes = field(init=False, default=b'')

    @property
    def socket(self):
        return self._socket

    @override
    def emit(self, event: str, *args: object, **kwargs: object):
        self._send_buffer += self._encode(event, *args, **kwargs)

    def _recv(self):
        """
        :private:

        Receive data from the socket and decode it.
        Trigger the events corresponding to the decoded data.

        :return: True if the socket is still connected, False otherwise.
        """
        while True:
            try:
                buffer = self._socket.recv(self.buffer_size)
            except BlockingIOError:
                break
            if not buffer:
                return False
            self._recv_buffer += buffer
            if len(buffer) < self.buffer_size:
                break
        while (pkt := self._decode()) is not None:
            if pkt == "EOF":
                return False
            self._trigger_event(pkt.event, *pkt.args, **pkt.kwargs)
        return True

    def _encode(self, event: str, *args: object, **kwargs: object):
        """
        :private:

        Encode the event `event` with `args` and `kwargs` as arguments.

        :param event: The event to encode.
        :param args: The arguments to pass to the event's callbacks.
        :param kwargs: The keyword arguments to pass to the event's callbacks.
        :return: The encoded event.
        """
        pkt = pkl.dumps(
            Message(event=event, args=args, kwargs=kwargs),
        )
        return len(pkt).to_bytes(8, sys.byteorder) + pkt

    def _decode(self):
        """
        :private:

        Decode the next event in the receive buffer, if any.

        :return: The first decoded event, or `None` if there is no event
            to decode.
        """
        if len(self._recv_buffer) < 8 or (pkt_size := int.from_bytes(
            self._recv_buffer[:8],
            sys.byteorder,
        )) > len(self._recv_buffer) + 8:
            return None
        if pkt_size:
            pkt = cast(Message, pkl.loads(self._recv_buffer[8:pkt_size+8]))
        else:
            pkt = "EOF"
        self._recv_buffer = self._recv_buffer[pkt_size+8:]
        return pkt

    def _send(self) -> None:
        """
        :private:

        Send the data in the send buffer to the socket, or as much as possible.
        """
        if self._send_buffer:
            bytes = self._socket.send(self._send_buffer)
            self._send_buffer = self._send_buffer[bytes:]
