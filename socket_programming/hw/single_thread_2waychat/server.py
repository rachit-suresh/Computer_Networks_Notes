import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

interface="127.0.0.1"
port=12345
sock.bind((interface,port))
print(f"Socket bound to the port: {port}")


sock.listen()
print("socket is listening")

conn, addr = sock.accept()
print(f"got conn from client: {addr}")

while True: 
  data = conn.recv(1024)
  if not data:
    print("Nice talking to you. Bye!!")
    break
  print(f"Data from client = {data.decode()}")
  out_data = input()
  conn.send(out_data.encode())
  if out_data=="exit()":
    break

conn.close()
sock.close()
