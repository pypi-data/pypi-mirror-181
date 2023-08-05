from typing import Optional
from typing import List
from typing import Union
from pydantic import Field

from ._models import Section


class Socket(Section):
    """
    Systemd [Socket] Section Directives
    """

    listen_stream: Optional[Union[str, List[str]]] = Field(
        None,
        title="ListenStream",
        description="This defines an address for a stream socket which supports sequential, reliable "
                    "communication. Services that use TCP should use this socket type."
    )
    listen_datagram: Optional[Union[str, List[str]]] = Field(
        None,
        title="ListenDatagram",
        description="This defines an address for a datagram socket which supports fast, unreliable "
                    "communication packets. Services that use UDP should set this socket type."
    )
    listen_sequential_packet: Optional[Union[str, List[str]]] = Field(
        None,
        title="ListenSequentialPacket",
        description="This defines an address for sequential, reliable communication with max length "
                    "datagrams that preserves message boundaries. This is found most often for Unix sockets."
    )
    listen_fifo: Optional[Union[str, List[str]]] = Field(
        None,
        title="ListenFIFO",
        description="Along with the other listening types, you can also specify a FIFO buffer instead of a socket."
    )
    accept: Optional[bool] = Field(
        None,
        title="Accept",
        description="This determines whether an additional instance of the service will be each connection. "
                    "If set to false (the default), one instance will handle all connections."
    )
    socket_user: Optional[str] = Field(
        None,
        title="SocketUser",
        description="With a Unix socket, specifies the owner of the socket. This will be the root user if left unset."
    )
    socket_group: Optional[str] = Field(
        None,
        title="SocketGroup",
        description="With a Unix socket, specifies the group owner of the socket. This will be the root "
                    "group if neither this or the above are set. If only the SocketUser= is set, "
                    "systemd will try to find a matching group."
    )
    socket_mode: Optional[str] = Field(
        None,
        title="SocketMode",
        description="For Unix sockets or FIFO buffers, this sets the permissions on the created entity."
    )
    service: Optional[str] = Field(
        None,
        title="Service",
        description="If the service name does not match the .socket name, the service can be "
                    "specified with this directive."
    )

    class Config:
        fields = {
            'ListenStream': 'listen_stream',
            'ListenDatagram': 'listen_datagram',
            'ListenSequentialPacket': 'listen_sequential_packet',
            'ListenFIFO': 'listen_fifo',
            'Accept': 'accept',
            'SocketUser': 'socket_user',
            'SocketGroup': 'socket_group',
            'SocketMode': 'socket_mode',
            'Service': 'service'
        }
