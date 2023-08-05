""" UDP Server."""

import select
import socket


def recv_timeout(sock: socket.socket, bytes_to_read: int, timeout_seconds: int):
    """
    Receive function with timeout.

    Parameters
    ----------
    sock:
        The socket to receive data from.
    bytes_to_read:
        Number of bytes to read per recv.
    timeout_seconds
        Timout in seconds before an error is raised.

    Returns
    -------
        The data from the socket.

    Raises
    ______
    socket.timeout
        Raised if no data is received from the socket within timeout_seconds.
    """
    sock.setblocking(False)
    ready = select.select([sock], [], [], timeout_seconds)
    if ready[0]:
        return sock.recvfrom(bytes_to_read)

    raise socket.timeout(f'No data received within {timeout_seconds}.')


class UdpServer:
    """
    Server to use with UDP protocol.
    """

    def __init__(self, responder):
        self._responder = responder
        self.ip = "127.0.0.1"
        self.port = 20001
        self.buffer_size = 1024
        self.is_running = False
        self._run = False

    def run(self, timeout: int = 1):
        """
        Start the server.

        Parameters
        ----------
        timeout
            Time in seconds within which data must be received.
        """
        self._run = True
        udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.bind((self.ip, self.port))
        print("UDP server up and listening")
        self.is_running = True

        while self._run:
            try:
                message_from_client, client_address = recv_timeout(udp_socket, self.buffer_size, timeout)
            except socket.timeout:
                continue
            message_from_client = message_from_client.decode()
            print(f'Message from {client_address}: "{message_from_client}"')
            if message_from_client == 'MOCKSERVER:STOP':
                print('Waiting for server to stop...')
                self._run = False
            else:
                answer = self._responder.respondTo(message_from_client)
                print(f'  Sending answer: "{answer}"')
                print(type(udp_socket.sendto))
                udp_socket.sendto(str.encode(answer), client_address)

        udp_socket.close()
        self.is_running = False
        print('Server stopped.')
