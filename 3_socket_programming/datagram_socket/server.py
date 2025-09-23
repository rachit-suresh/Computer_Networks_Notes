import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

interface="127.0.0.1"
port=12345
sock.bind((interface,port))


data1, addr1=sock.recvfrom(1024)
data2, addr2=sock.recvfrom(1024)
print(f"data from client({addr1}) = {data1.decode()}")
print(f"data from client({addr2}) = {data2.decode()}")


#udp preserves message boundary, it not a stream 