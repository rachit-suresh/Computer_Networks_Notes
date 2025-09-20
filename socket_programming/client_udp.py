import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:  
  data=input()
  sock.sendto(data.encode(),("127.0.0.1",12345))

