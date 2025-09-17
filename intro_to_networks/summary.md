# Computer Networks & Systems - Summary Notes

## System Communication (Computer-Printer)

### Driver Architecture

- **Kernel Driver (sys file)**: Ring 0 level, direct hardware access
- **User-mode Driver (dll)**: Ring 3 level, safe abstraction layer
- **Communication**: IRPs for kernel-user mode interaction

### Virtual Memory Management

- **Virtual Address Space**: Each process isolated (user space + kernel space)
- **Page Tables**: VA to PA translation, demand paging
- **Protection**: Kernel space inaccessible from user mode

### Exception Handling

- **Protection Faults**: Invalid memory access triggers exception
- **Interrupt Service Routines**: Hardware/software interrupts
- **System Calls**: Controlled kernel entry points

### Printing Process

1. **Application**: CreateFile → GetPrinter → StartDocPrinter
2. **Spooler Service**: Queue management, EMF conversion
3. **Driver Processing**: GDI rendering, device commands
4. **Hardware Interface**: Port monitors, bidirectional communication

## Network Communication

### Protocol Fundamentals

- **Protocol**: Rules enabling device communication
- **Types**: Physical protocols, Logical/Software protocols
- **Necessity**: Establishes communication standards like human language

### Core Network Problems (18 Key Challenges)

1. **Address Discovery**: How browser finds server address
2. **Server Selection**: Multiple servers, routing decisions
3. **Identity Management**: Server-client recognition
4. **Global Addressing**: Unique server identification
5. **Path Finding**: Route discovery across router mesh
6. **Optimal Routing**: Shortest path vs load balancing
7. **Dynamic Statistics**: Real-time device status tracking
8. **Data Chunking**: Large data transmission strategies
9. **Packet Routing**: Independent packet navigation
10. **Metadata Efficiency**: Optimal packet header design
11. **Packet Loss**: Connection breaks, data corruption
12. **Error Detection**: Corruption identification mechanisms
13. **Error Correction**: Corrupted error messages
14. **Path Resilience**: Router failure handling
15. **Security**: Data privacy during transmission
16. **Encryption**: Secure key exchange protocols

### Network Addressing

#### IP Addresses

- **IPv4**: 32-bit (a.b.c.d), 4.3 billion addresses
- **IPv6**: 128-bit, expanded address space
- **Transition**: IPv4-IPv6 compatibility challenges

#### Port Numbers

- **Purpose**: Process identification on devices
- **Function**: Routes data to specific applications
- **Example**: google.com:80 (HTTP), google.com:81 (blocked)

### Network Architecture Models

#### OSI Model (7 Layers)

1. **Physical**: Data transmission
2. **Data Link**: Direct device communication (MAC addresses)
3. **Network**: Efficient routing (IP, routers, algorithms)
4. **Transport**: Reliable delivery (TCP)
5. **Session**: Connection management (cookies, tokens)
6. **Presentation**: Encryption, compression (SSL/TLS)
7. **Application**: End-user services (HTTP)

#### TCP/IP Model (IP Suite)

- **Link**: Combined physical + data link
- **Internet**: Renamed network layer
- **Transport**: Same as OSI
- **Application**: Combined application + presentation + session

## Key Concepts Summary

### System Level

- **Abstraction Layers**: Hardware → Kernel → User applications
- **Memory Protection**: Virtual addressing, privilege levels
- **Communication**: IRPs, system calls, interrupts
- **Resource Management**: Spooling, queuing, scheduling

### Network Level

- **Protocol Stack**: Layered communication models
- **Addressing**: Unique identification (IP + Port)
- **Routing**: Path optimization across networks
- **Reliability**: Error detection, correction, retransmission
- **Security**: Encryption, authentication, authorization

### Fundamental Principles

- **Abstraction**: Hide complexity through layered models
- **Modularity**: Separate concerns into distinct layers
- **Standards**: Common protocols enable interoperability
- **Reliability**: Multiple mechanisms ensure data integrity
- **Scalability**: Architecture supports global networks
