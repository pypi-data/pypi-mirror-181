""" TCP Server."""

import socket

import genericserver.responders


class TcpServer:
    """
    Server to use with TCP protocol.
    """
    def __init__(self, responder: genericserver.responders.MockResponder):
        self._responder = responder
        self.ip = "127.0.0.1"
        self.port = 20001
        self.buffer_size = 1024
        self.is_running = False
        self._run = False

    def run(self):
        """
        Start the server.
        """
        self._run = True
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((self.ip, self.port))
        tcp_socket.listen()
        print("TCP server up and listening")
        self.is_running = True

        conn, client_address = tcp_socket.accept()
        with conn:
            print(f"Connected from {client_address}")
            while self._run:
                message_from_client = conn.recv(self.buffer_size)
                if not message_from_client:
                    break
                message_from_client = message_from_client.decode()
                print(f'Message from {client_address}: "{message_from_client}"')
                if message_from_client == 'MOCKSERVER:STOP':
                    print('Waiting for server to stop...')
                    self._run = False
                else:

                    answer = self._responder.respondTo(message_from_client)
                    print(f'  Sending answer: "{answer}"')
                    conn.sendall(str.encode(answer))

        tcp_socket.close()
        self.is_running = False
        print('Server stopped.')
