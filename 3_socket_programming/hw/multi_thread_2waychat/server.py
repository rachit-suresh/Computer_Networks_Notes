import socket
import threading

def receive_client(conn, addr):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected")
                break
            print(f"Client: {data.decode()}")
    except Exception as e:
        print(f"Receive error: {e}")

def send_client(conn, addr):
    try:
        while True:
            data = input()
            conn.send(data.encode())
            if data == "exit()":
                break
    except Exception as e:
        print(f"Send error: {e}")

def handle_client(conn, addr):
    print(f"Connected to client: {addr}")
    
    recv_thread = threading.Thread(target=receive_client, args=(conn, addr))
    send_thread = threading.Thread(target=send_client, args=(conn, addr))

    recv_thread.start()
    send_thread.start()
    
    recv_thread.join()
    
    print(f"Chat ended with {addr}")
    conn.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 12345))
sock.listen()
print("Server listening on port 12345")

try:
    conn, addr = sock.accept()
    handle_client(conn, addr)
except KeyboardInterrupt:
    print("\nServer shutting down")
finally:
    sock.close()