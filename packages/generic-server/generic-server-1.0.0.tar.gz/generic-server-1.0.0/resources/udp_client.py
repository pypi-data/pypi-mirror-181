import socket

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
bytes_sent = sock.sendto(str.encode('Hello World!'), ('localhost',20001))
msgFromServer = sock.recvfrom(1024)
sock.close()