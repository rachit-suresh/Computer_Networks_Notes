import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#address family is if we want to create scoket over ipv4(AF_INET) or ipv6, type is either stream sockets or datagram which only mean how the data flow like stream = continuous, protocol can be any protocol you provide tcp,udp, custom and tcp is default for stream and udp default for datagram, fileno - everything in linux is treated as a file so its somthing related to that
print("Socket created")

interface="127.0.0.1"
port=12345
sock.bind((interface,port))
print(f"Socket bound to the port: {port}")


sock.listen()#optionally takes in a number as a parameter which represents how many pending connection our server can hold on its side, all the above code is going to happen on the main thread so if a so a second client will not be able to connect if a client has already connected unless we do something from our side
print("socket is listening")

conn, addr = sock.accept()# return s2 things, a socket object using which we will communicate with client and also give info od client like ip, port etc, main socket's job(sock) is only to accept the connection, when we accept it gives us the new socket object(conn) using which we will comm, why should a new socket object be created? we want to keep the main socket free to avoid talking to only one server,main socket has to keep listening so a new socket object has been provided
print(f"got conn from client: {addr}")

while True: 
  data = conn.recv(1024)#how many maximum bytes are you okay to receive from server 
#  if data.decode() == "exit()":
  if not data:
    print("Nice talking to you. Bye!!")
    break
#conn.recv is will continuosuly wait when it receives no data since it is blocking in nature nothing after it will execute, but notice that in the above code, even when we change the code to check for if not data, it works because after client is down server receives no data when it waits to receive, but isnt this contradictary, just above i said that  when it receives no data since it is blocking in nature nothing after it will execute, how is it entering the if codn? This is because when our client breaks it goes to the next line and calls sock.close() this then sends one last empty data to server indictaing that the client is done and is breaking off the connection since it is using tcp which is connection oriented, so client sends a finish packet which contains empty byte inside it so conn.recv receives that empty byte then goes to if codn and eventually sock is closed

  print(f"Data from client = {data.decode()}")# data is in binary when it travels so we decode it on server side and encode on client side

conn.close()
sock.close()
#we technically dont have to do this since when rpogram ends garbage collector clears it anyway but its good pracctice to do so, this is okay when we are doing somthing this simple but in production level this will cause a samll memory leak and even it can escalate and crash the whole server since we cant depend on os to reclaim memory immediately

#if i put the while loop beofre listen then i get  ConnectionAbortedError: [WinError 10053] An established connection was aborted by the software in your host machine error when i try to send data multiple time, why?

#also when i close the client while server is running i this weird output Data from client= in an infinite loop why and why i the data empty?
#conn knows that the connection is broken so when we try to call .recv on a socket object whose connection is broken it simply sends back an empty byte and since we are in an infinite while loop the above phenomenon happens


#how does it differentiate between the final empty byte and normal no data, why send empty byte why not something else, search about how this works in detail