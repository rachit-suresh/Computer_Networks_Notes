Data travels as multiple chunks over the network
Why?
1. Data at the end of the day is 1s and 0s and is travelling between computers, if a line b/w computers is continuosly occupied by my data then its problematic for others tryna send data we block the lines, technically one line can allow for multiple peoplr to send data through it at the same time but even that is limited like 4 or 16


2. If data gets corrupted we have to send the whole data again

In data packets we only have to resend the specific chunk which is corrupted


3. While the data is hopping routers whlile travelling to your destination and a router on the route its travelling in fails then the whole data just vanishes since there is no db storing it, we have to send whole data again

The routers keep talking to each other so in case of using data pakcets if a router gets to know that the next router failed, it can reroute the rest of the packets through another route, a few packets may get lost who travelled before rerouting but we only have to resend that not the whole data 


4. In our devices, routers, switches etc everyone has a limited amount of memeory and routers have to receive process and forward the data, so what if a hugee data packet reaches a router, the size of data packet exceedes router's memory, so the router cannot do anything in the scenario, it cant even break the data cuase to do that also it has to first take in and process the data

This is why we divde data into chunks, by convention these chunks are refered to as data packets, it is a popular name but not 100 percent technically accurate, so in reality what is it called?why?
TCP header + payload = TCP segment
IP header + TCP header + payload = IP packet
Ethernet header + IP header + TCP header + payload + trailers = Ethernet Frame

in reality its not only the packet moving from point to point but its the whole frame

# Data packets
The below discussion is more specific to tcp

### 1. Headers
Actual data dosent know where to go on its own and lacks any such info so we have metadata stored in headers

The header itself is divided into three parts, sub headers, each layer is directly responsible to handle some of these fields, payload gets created at application layer, the transport layer adds TCP header, network/internet layer adds the IP header and then the link layer is repossible to add the ethernet header, link layer also adds the trailers, why are there checksums in 3 diff locations(tcp,ip header and trailer)?


#### TCP header
1. Seq numbers

2. Ack number 

3. Source port

4. Destination port 

5. Control flag : Fin(the last packet when the connection closes), Urgent(router receives so much data some packets have higher priority), PSH(push, sender side is telling the receiver side to not store all of this in buffer and then reconstruct it as soon as you receive it just push it directly to application), etc

6. Checksum(calsulated value derived from data that serves as the fingerprint for that data)(present in tcp header, ip header and trailer)
Not specific to networking, general concept used in it industry to check data integrity or verify data

Server side(performs some mathematical calc on the data)(this value is put in the packet)
Client side(performs same calc on data)(compare this value with value stored in packet)

Checksum in TCP header is used to verify the TCP segment
  Only calculated at destination
Checksum in IP header is used to verify only the IP header
  Data inside ip header is very imp as its used to actually route the data, and is calculated at each hop so they decided to exclude TCP header and payload data from the checksum
Checksum in trailer is used to verify the complete ethernet frame



All these checksums use the Internet checksum algorithm

Lets see the process of TCP checksum

We divide the bits in 16 bit chunks
Add them all together(using wrap arounf arithmetic)
Calc 1s complement of the addition
Store this value in packet

On the receivers side, it does not have to do the one's complement, since adding a number with its one's complement always gives all 1's which is considered to be zero. but why is all 1's considered zero?

11001011111001011001110100011000

 1100101111100101 + 1001110100011000 = 10110100111111101

Now we have an extra bit, the design decision could be to drop that bit but it decided to use wrap around arithmetic

0110100111111101 + 1 = 0110100111111110

1's complement -> 1001011000000001 -> checksum

but we are doing simple addition here even if like a 1 becomes 0 and vice versa of the same place so even if the data is corrupted it shows that data is proper but this is acceptable in the internet checksum algoithm, in this case they traded complexity and more integrity for time since so much data is coming in processing all of that with a complex algorithm is very time and  resource consuming

one of the more complex algorithms is caled crc algorithm research about it if you want to




---------------------------------------------------------------------------------
#### IP header
1. Src IP

2. Dest IP

3. protocol

4. version(ipv4/ipv6)

5. checksum

----------------------------------------------------------------------------------
#### Ethernet header
1. Identification(data packet  itself can be broken down into mutiple packets so this helps us identify them)

  When a packet/frame moves from device to device, each device has a limited amount of memory,a limit to how much a device can process and transfer through its network interface
  MTU(Max Transmissible Unit)(what maximum size data packet can be processed by that interface)
  If a packet arrives with data>MTU  router further breaks this packet into smaller chunks called fragments through fragmentation
  So to help us combine this again later, each fragment is assigned the same identification number
  There is a field in the packet called DF(dont fragment), if value of DF is true then router does not fragment it and simply drops the packet since it cannot process it, but why does DF even exist in the first place?

(the network interfaces of our devices have a specific mac addresses permanently burned into them by manufacturer, purpose of a mac addr is when 2 dives comunicate directly in the same network  they dont use ip addr they use mac addr, the ip addr is used to find mac addr)
2. Dest MAC addr(our device when sending req to google dosent need to know its addr but since it is not in our network, it needs to knows the mac of the local router which we have and the router needs to know mac of next device and so on so the dest mac keeps chnges every hop)

3. Src MAC addr


Source-->A--->B--->C--->Dest
At source dest MAC will be of A and src MAC will be of source
At A it will be B and src will be A(when this changes the trailer checksum also changes)
And so on

Anytime our data is moving from one device to another with every hop the ehternet header is stripped away and a new ethernet header is given and trailer checksum is recalculated

But h=what if during the stripping off reapplication and recalculation steps the actual data(payload) changed, during the recaluculation we include would say that the corrupted one is the correct one so trailer checksum is not used to verify the payload data at final dest

### 2. Payload
Actual data we have to send
### 3. Trailers
Also contains some metadata and checksum


check out wireshark 
