import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.bind(("127.0.0.1",12345))

sock.listen()
conn, addr = sock.accept()

data1= conn.recv(1024)
data2= conn.recv(1024)
data3= conn.recv(1024)

print(f"data1={data1.encode()}")
print(f"data2={data2.encode()}")
print(f"data3={data3.encode()}")

sock.close()


#the output comes out to be data1=lollollol data2= data3= , why?
#tcp streams the data it does not preserve message boundaries, it flows like water, server dosent know that lol was the first message client wanted to send hello was the second message and so on, server dosent know where first message is starting or ending