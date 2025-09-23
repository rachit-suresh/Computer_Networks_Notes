import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(("127.0.0.1",12345))#server address

while True:
  data=input()
  sock.send(data.encode())
  if data=="exit()":
    break
  in_data=sock.recv(1024)
  if in_data.decode()=="exit()":
    print("sever broke off conn")
    break
  print(f"hey look its the server talking back: {in_data.decode()}")


sock.close()


#when we try to type in the client side when its the server's turn to send messages, it behaves weirdly cuase as soon as the it receives data from server, it instantly sends he message i typed by mistake as though there was a input buffer in which it stored it in
''' 
Your current client and server are designed for a very strict "speak-and-wait-for-reply" turn-taking:

Client:

input() - Wait for user to type.

send() - Send user's message.

recv() - Wait for server's reply.

print() - Display server's reply.

Repeat.

Server (for one client):

recv() - Wait for client's message.

print() - Display client's message.

input() - Wait for user to type.

send() - Send user's message.

Repeat.

What happens if you type early on the client side?

Client: You type hi and press Enter. (This goes into the OS's keyboard buffer, but input() only consumes it when called.)

Client: input() is called, consumes hi.

Client: send('hi').

Server: recv() gets hi.

Server: print('hi').

Server: input() - Server user now types hello.

Server: send('hello').

Client: recv() gets hello.

Client: print('hello').

Client: input() - This is where you expect to type your next message.

Client: But because you typed something earlier (e.g., wassup or hey) while the server was typing, that input is sitting in the keyboard buffer provided by your terminal. When input() is called here, it instantly consumes wassup from the buffer, not waiting for new input.

Client: send('wassup') - It sends the "mistake" message.

Server: recv() gets wassup.

Server: print('wassup').

Server: input() - Waits for its next message.

This creates the illusion that the client is "instantly sending" a buffered message. It's not a bug, but a direct consequence of input() consuming whatever is ready in the terminal's input stream when it's called.

The Root Cause: Synchronous Blocking I/O
Both input() and recv() are blocking calls.

input() waits indefinitely until the user types something and presses Enter.

recv() waits indefinitely until data arrives on the socket.

Because your code executes them one after another in a single thread, it creates a rigid, synchronous "ping-pong" where one side must wait for the other. If one side sends multiple messages quickly, the other side will receive them quickly when its recv() is finally called, but its input() will still block until the user types.
'''
