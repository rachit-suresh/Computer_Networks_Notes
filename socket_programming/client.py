import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(("127.0.0.1",12345))#server address

while True:
  data=input()
  sock.send(data.encode())
  if data=="exit()":
    break


sock.close()