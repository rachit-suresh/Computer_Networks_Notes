1. dig

![alt text](image-1.png)

- hits dns server recursive resolver and fetches final ip
- works in a query ans fashion

![alt text](image.png)

- The number 186 is the TTL for cache and IN means internet, A means records of mapping(discussed in dns)
- used by dev ops engineers to see if dns mapping has happened or not

![alt text](image-2.png)

- trace traces the whole flow of dns

root servers
![alt text](image-3.png)

tld
![alt text](image-4.png)

ans
![alt text](image-5.png)

google servers
![alt text](image-6.png)

2. nslookup

- simpler version of dig

3. host 

- even simpler version of dig

4. telnet

- creates a tcp conn with a remote server and then we can communicate with it using http

![alt text](image-7.png)

5. ifconfig(interface config)

- shows all network interfaces on system

![alt text](image-8.png)

6. iftop

- shows the amount of bandwidth that is getting utilised for every conn trying to tLalk to our system

![alt text](image-9.png)

![alt text](image-11.png)

- good tool to figure out if someone is unnecessarily trying to hit our servers

7. tcpdump

![alt text](image-10.png)

- what wireshark was but without gui, captures all data packets coming on all interfaces

![alt text](image-12.png)