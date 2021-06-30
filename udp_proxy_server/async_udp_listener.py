import socket
import struct
import asyncio
from asyncio.protocols import DatagramProtocol


class MulticastServerProtocol(DatagramProtocol):
    def datagram_received(self, data, addr):
        print(f"Message from {addr[0]}:{addr[1]} :  {data.decode('utf-8')}")


class AsyncUDPMulticastListener:
    def __init__(self, multicast_group, multicast_port):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.loop = asyncio.get_event_loop()

    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        group = socket.inet_aton(self.multicast_group)
        sock.bind((self.multicast_group, self.multicast_port))
        mreq = group + struct.pack('=I', socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return sock

    def run(self):
        listen = self.loop.create_datagram_endpoint(MulticastServerProtocol, sock=self.create_socket())
        self.loop.run_until_complete(listen)
        self.loop.run_forever()
        self.loop.close()


if __name__ == '__main__':
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    server = AsyncUDPMulticastListener(MCAST_GRP, MCAST_PORT)
    server.run()
