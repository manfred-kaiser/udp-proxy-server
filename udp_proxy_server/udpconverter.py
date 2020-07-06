import socket
from select import select
import struct
import logging


class UDPConverter():

    def __init__(self, server_address, target_address, buffer_size=4096, multicast_group=None, single_connection=False):
        self.server_address = server_address
        self.target_address = target_address
        self.buffer_size = buffer_size
        self.multicast_group = multicast_group
        self.clients = {}
        self.sockets = {}
        self.single_connection = single_connection

    def clean_address(self, address):
        if self.single_connection:
            address = '127.0.0.1'
        if address in self.clients:
            del self.clients[address]
            logging.debug("removed address %s", address)
        sock_key = None
        for k, v in self.sockets.items():
            if address == v:
                sock_key = k
        if sock_key:
            del self.sockets[sock_key]
            logging.debug("removed socket for address %s", address)

    def create_udp_socket(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.server_address)

        if self.multicast_group:
            group = socket.inet_aton(self.multicast_group)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            sock.setsockopt(
                socket.IPPROTO_IP,
                socket.IP_ADD_MEMBERSHIP,
                mreq
            )
        return sock

    def get_remote(self, *, sock=None, address=None):
        if self.single_connection:
            address = '127.0.0.1'
        if sock:
            if sock in self.sockets:
                return self.sockets[sock]
        if address:
            if address not in self.clients:
                self.clients[address] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clients[address].connect(self.target_address)
                self.sockets[self.clients[address]] = address
            return self.clients[address]
        return None

    def run(self):
        sock = self.create_udp_socket()
        self.sockets[sock] = None

        while True:
            for s in select(self.sockets.keys(), [], [])[0]:
                address = None
                try:
                    if s.type == socket.SOCK_DGRAM:
                        data, address = s.recvfrom(self.buffer_size)
                        if not data:
                            break
                        self.get_remote(address=address).sendall(data)
                    else:
                        data = s.recv(self.buffer_size)
                        if not data:
                            break
                        if not self.single_connection:
                            sock.sendto(data, self.get_remote(sock=s))
                except (ConnectionRefusedError, BrokenPipeError):
                    if address:
                        self.clean_address(address)
                except Exception:
                    logging.exception("Fehler UDP")
