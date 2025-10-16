import socket
import threading

def send_msg(sock):
    try:
        while True:
            data = input()
            sock.send(data.encode())
            if data == "exit()":
                break
    except Exception as e:
        print(f"Send error: {e}")

def recv_msg(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("Server disconnected")
                break
            if data.decode() == "exit()":
                print("Server ended session")
                break
            print(f"Server: {data.decode()}")
    except Exception as e:
        print(f"Receive error: {e}")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(("127.0.0.1", 12345))
    print("Connected to server")
    
    send_thread = threading.Thread(target=send_msg, args=(sock,))
    recv_thread = threading.Thread(target=recv_msg, args=(sock,))
    
    send_thread.start()
    recv_thread.start()
    
    recv_thread.join()
    
    print("Chat ended")
    
except KeyboardInterrupt:
    print("\nClient interrupted")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()

    