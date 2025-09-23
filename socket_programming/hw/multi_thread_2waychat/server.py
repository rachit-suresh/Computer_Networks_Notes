import socket
import threading

def receive_client(conn, addr):
    """
    This function runs in its own thread to receive messages from the client.
    It's kept as similar to your original as possible.
    """
    try:
        # Loop forever to keep listening for messages.
        while True:
            # Wait to receive data from the client. This is a blocking call.
            data = conn.recv(1024)
            
            # NECESSARY CHANGE: Check if the client disconnected gracefully.
            # If recv() returns no data (an empty byte string), it means the client
            # has closed their side of the connection. We must exit the loop.
            if not data:
                print(f"Client {addr} has disconnected.")
                break # Exit the while loop, which will end this thread.
                
            # If we received data, decode it from bytes to a string and print it.
            print(f"Data from client {addr} = {data.decode('utf-8')}")
            
    except ConnectionResetError:
        # NECESSARY CHANGE: This handles abrupt disconnects (e.g., client crashes).
        print(f"Client {addr} connection ended abruptly.")
    except Exception as e:
        # NECESSARY CHANGE: Catches any other unexpected errors.
        print(f"An error occurred in receive_client for {addr}: {e}")

def send_client(conn, addr):
    """
    This function runs in its own thread to send messages to the client.
    It's kept as similar to your original as possible.
    """
    try:
        # Loop forever to keep sending messages.
        while True:
            # Wait for the server operator to type a message. This is a blocking call.
            data = input()
            
            # Send the user's message, encoded from a string into bytes.
            conn.send(data.encode('utf-8'))

            # Check if the server operator wants to end the chat.
            if data == "exit()":
                break # Exit the loop, which will end this thread.

    except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
        # NECESSARY CHANGE: These errors occur if the connection is already
        # broken when we try to send. This allows the thread to exit cleanly.
        print(f"Connection to {addr} is lost. Cannot send message.")
    except Exception as e:
        print(f"An error occurred in send_client for {addr}: {e}")

def handle_client(conn, addr):
    """
    This is your original function to manage the two threads for a single client.
    """
    print(f"Starting chat with client: {addr}")
    
    # Create the two threads, one for receiving and one for sending.
    recv_thread = threading.Thread(target=receive_client, args=(conn, addr))
    send_thread = threading.Thread(target=send_client, args=(conn, addr))

    # Start both threads so they run at the same time.
    recv_thread.start()
    send_thread.start()
    
    # NECESSARY CHANGE: Wait for the receive thread to finish.
    # The receive thread is the best one to monitor because it will naturally
    # end when the client disconnects. The send_thread would be stuck on input().
    recv_thread.join()
    
    # After the session ends, we can clean up.
    print(f"Chat session with {addr} has ended.")
    conn.close() # Close the connection here, in one central place.

# --- Main Server Execution ---
# This part is kept very similar to your code.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

interface = "127.0.0.1"
port = 12345
sock.bind((interface, port))
print(f"Socket bound to the port: {port}")

sock.listen()
print("socket is listening")

# This is a one-client server, so it will accept one connection and then focus on it.
# The 'try' block helps us catch Ctrl+C to shut down cleanly.
try:
    # Wait for a single client to connect. This is a blocking call.
    conn, addr = sock.accept()
    
    # We are not creating a thread for handle_client itself,
    # because this server is dedicated to only one client.
    # We just call the function directly.
    handle_client(conn, addr)
    
except KeyboardInterrupt:
    print("\nServer is shutting down.")
finally:
    # This ensures the main listening socket is always closed.
    sock.close()
    print("Server socket closed.")