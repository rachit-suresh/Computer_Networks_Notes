import socket
import threading

#we use a try catch block to gracefully handle an error, without it the necessary clean up code conn.close() might not run causing leaks or incase our worker thread had acquired a lock on a resource in case of a try catch block we can release the lock in finally to avoid deadlocks, we can also add code in except block to roll back change and prevent corrupted data from cauing more errors
def handle_client(conn,addr):
  try:
    print(f"got conn from client: {addr}")
    while True: 
      data = conn.recv(1024)
      if not data:
        print("Nice talking to you. Bye!!")
        break
    print(f"Data from client{addr} = {data.decode()}")
  except ConnectionResetError:
    print(f"Client {addr} disconnected forcefully")#incase the client connection terminates abruptly like in case of a keyboard interrupt, closing the terminal etc, it is a very common error
  except Exception as e:
    print(f"an error: {e} occured with client {addr}")#to catch all other errors
  finally:
    conn.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

interface="127.0.0.1"
port=12345
sock.bind((interface,port))
print(f"Socket bound to the port: {port}")

sock.listen()
print("socket is listening")

while True:
  conn, addr = sock.accept()
  thread=threading.Thread(target=handle_client,args=(conn,addr))
  thread.start()
  print(f"active connections: {threading.active_count()-1}")
