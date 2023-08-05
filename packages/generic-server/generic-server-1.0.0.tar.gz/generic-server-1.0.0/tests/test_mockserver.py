"""Test the MockServer."""
from unittest.mock import Mock
import socket

from genericserver.mockserver import MockServer
from genericserver.responders import MockResponder
from genericserver.tcpserver import TcpServer
from genericserver.udpserver import UdpServer


def test_init_udpServer():
    my_server = MockServer(protocol='udp', responder='reflect')
    assert isinstance(my_server, MockServer)
    assert isinstance(my_server.server, UdpServer)
    assert isinstance(my_server.server._responder, MockResponder)


def test_init_tcpServer():
    my_server = MockServer(protocol='tcp', responder='reflect')
    assert isinstance(my_server, MockServer)
    assert isinstance(my_server.server, TcpServer)
    assert isinstance(my_server.server._responder, MockResponder)


def test_udp_run_got_stop(mocker):
    # set up mocks
    mock_sock = mocker.patch('genericserver.udpserver.socket.socket')
    mock_sock.return_value.bind.return_value = 'bound'
    mock_sock.return_value.setblocking.return_value = None
    mock_sock.return_value.recvfrom.return_value = (str.encode('MOCKSERVER:STOP'), ('127.0.0.1', 20001))

    mocker.patch("genericserver.udpserver.select.select", return_value=[True, True])

    # run mock server
    my_server = MockServer()
    my_server.run()

    mock_sock.assert_called_once()
    mock_sock.return_value.recvfrom.assert_called_once()


def test_udp_reflect(mocker):
    # set up mocks
    request = str.encode('test')
    client_addr = ('127.0.0.1', 20001)
    mock_sock = mocker.patch("genericserver.udpserver.socket.socket")
    mock_sock.return_value.bind.return_value = 'bound'
    mock_sock.return_value.setblocking.return_value = None
    mock_sock.return_value.recvfrom.side_effect = [(request, client_addr),
                                                   (str.encode('MOCKSERVER:STOP'), client_addr)]
    mock_sock.return_value.sendto.return_value = None

    mocker.patch("genericserver.udpserver.select.select", return_value=[True, True])

    # run mock server
    my_server = MockServer()
    my_server.run()

    mock_sock.assert_called_once()
    mock_sock.return_value.sendto.assert_called_once_with(request, ('127.0.0.1', 20001))
    assert mock_sock.return_value.recvfrom.call_count == 2


def test_tcp_run_got_stop(mocker):
    # set up mocks
    mock_conn = Mock()
    mock_conn.__enter__ = lambda *args: True
    mock_conn.__exit__ = lambda *args: True
    mock_conn.recv.return_value = str.encode('MOCKSERVER:STOP')

    mock_sock = mocker.patch('genericserver.udpserver.socket.socket')
    mock_sock.return_value.setsockopt.return_value = None
    mock_sock.return_value.bind.return_value = None
    mock_sock.return_value.listen.return_value = None
    mock_sock.return_value.setblocking.return_value = None
    mock_sock.return_value.accept.return_value = (mock_conn, ('127.0.0.1', 20001))

    mocker.patch("genericserver.udpserver.select.select", return_value=[True, True])

    # run mock server
    my_server = MockServer(protocol='tcp')
    my_server.run()

    mock_sock.assert_called_once()
    mock_sock.return_value.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mock_conn.recv.assert_called_once()


def test_tcp_reflect(mocker):
    request = str.encode('test')
    client_addr = ('127.0.0.1', 20001)

    # set up mocks
    mock_conn = Mock()
    mock_conn.__enter__ = lambda *args: True
    mock_conn.__exit__ = lambda *args: True
    mock_conn.recv.side_effect = [request,
                                  str.encode('MOCKSERVER:STOP')]
    mock_conn.sendall.return_value = None

    mock_sock = mocker.patch('genericserver.udpserver.socket.socket')
    mock_sock.return_value.setsockopt.return_value = None
    mock_sock.return_value.bind.return_value = None
    mock_sock.return_value.listen.return_value = None
    mock_sock.return_value.setblocking.return_value = None
    mock_sock.return_value.accept.return_value = (mock_conn, client_addr)

    mocker.patch("genericserver.udpserver.select.select", return_value=[True, True])

    # run mock server
    my_server = MockServer(protocol='tcp')
    my_server.run()

    mock_sock.assert_called_once()
    mock_sock.return_value.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mock_conn.sendall.assert_called_once_with(request)
    assert mock_conn.recv.call_count == 2
