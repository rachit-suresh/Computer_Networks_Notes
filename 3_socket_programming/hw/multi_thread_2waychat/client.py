import socket
import threading

def send_msg(sock):
    """
    This is your original function for sending messages from the client.
    """
    try:
        # Loop forever to allow typing multiple messages.
        while True:
            # Wait for the user to type a message.
            data = input()
            
            # Send the message to the server.
            sock.send(data.encode('utf-8'))
            
            # If the user types 'exit()', we want to shut down.
            if data == "exit()":
                break # Exit the loop, which will cause this thread to end.
    
    except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
        # NECESSARY CHANGE: If the server connection is lost, trying to send
        # will cause an error. This catches it so the thread can exit gracefully.
        print("Connection to the server has been lost.")
    except Exception as e:
        print(f"An error occurred in send_msg: {e}")

def recv_msg(sock):
    """
    This is your original function for receiving messages from the server.
    """
    try:
        # Loop forever to keep listening for server messages.
        while True:
            # Wait to receive data from the server.
            in_data = sock.recv(1024)
            
            # NECESSARY CHANGE: Check if the server disconnected.
            # An empty byte string means the server closed the connection.
            if not in_data:
                print("Server broke off the connection.")
                break # Exit the loop to end this thread.
                
            # If the server sent 'exit()', we also treat it as a disconnect.
            if in_data.decode('utf-8') == "exit()":
                print("Server has ended the session.")
                break # Exit the loop.
            
            # If we got a normal message, print it.
            print(f"Server says: {in_data.decode('utf-8')}")

    except (ConnectionAbortedError, ConnectionResetError):
        # NECESSARY CHANGE: This handles cases where the connection drops
        # or the socket is closed while we are waiting to receive.
        pass # We don't need to print an error, just exit the thread.
    except Exception as e:
        print(f"An error occurred in recv_msg: {e}")

# --- Main Client Execution ---
# This structure is the same as yours.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(("127.0.0.1", 12345))
    print("Connected to server. You can start chatting.")
    
    # Create your two threads, just like you did.
    # The comma in args=(sock,) is required to make it a tuple.
    send_thread = threading.Thread(target=send_msg, args=(sock,))
    recv_thread = threading.Thread(target=recv_msg, args=(sock,))
    
    # Start both threads to run concurrently.
    send_thread.start()
    recv_thread.start()
    
    # NECESSARY CHANGE: Wait for one of the threads to finish.
    # Joining the receive thread is a good strategy because it will
    # end if the server disconnects.
    recv_thread.join()
    
    print("Chat session has ended.")
    
except KeyboardInterrupt:
    print("\nClient interrupted.")
except Exception as e:
    print(f"An error occurred with the client: {e}")
finally:
    # NECESSARY CHANGE: Close the socket here in the main thread.
    # This is the crucial fix to your "double close" problem.
    # We close it only once, after we know the threads are done.
    sock.close()
    print("Socket closed.")


    '''finally:

      sock.close()'''#in this code we tried to close the same sock in both threads, when one thread calls sock.close(), the other thread tries to use or close it again, causing this error.Only close the socket once, after both threads finish.Remove sock.close() from the finally blocks in both thread functions.Close the socket in the main thread after both threads have joined.

    