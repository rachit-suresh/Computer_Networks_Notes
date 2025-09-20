import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(("127.0.0.1",12345))#server address

sock.send("lol".encode())
sock.send("lol".encode())
sock.send("lol".encode())


sock.close()