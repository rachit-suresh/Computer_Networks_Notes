import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


sock.sendto("hello1".encode(),("127.0.0.1",12345))
sock.sendto("hello2".encode(),("127.0.0.1",12345))
