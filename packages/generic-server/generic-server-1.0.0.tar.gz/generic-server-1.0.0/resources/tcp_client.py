import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 20001))
sock.sendall(str.encode('Hello World!'))
sock.recv(1024)
sock.close()