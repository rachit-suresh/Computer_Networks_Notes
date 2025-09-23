import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

interface="127.0.0.1"
port=12345
sock.bind((interface,port))

while True:
  data, addr=sock.recvfrom(1024)
  print(f"data from client({addr}) = {data.decode()}")

#why isnt addr encoded, how does it know where data is coming from