# Introduction to Computer Networks - Class Summary

## Computer Networks Definition

**Computer Networks:** A collection of connected devices that share data with each other.

- **Core Challenge:** Complexities arise when data needs to flow between different devices
- **Solution Approach:** Establish standardized communication protocols

## Protocols

**Definition:** Rules that help devices communicate with each other.

### Protocol Types

1. **Physical Protocols**

   - Define how data is physically transferred between devices
   - Handle electrical, optical, and mechanical aspects

2. **Logical/Software Protocols**
   - Primary focus of network communication studies
   - Define data format, structure, and communication procedures

## Core Network Communication Problems

Network communication involves solving several fundamental challenges:

### Primary Problem Areas

1. **Server Identification**

   - How to identify and locate servers on the internet

2. **Data Routing**

   - How to route data through complex network infrastructure

3. **Data Segmentation**

   - How to break large data into smaller, manageable chunks (packets)

4. **Reliability Management**

   - How to handle data corruption and packet loss during transmission

5. **Network Resilience**

   - How to manage network changes and failures dynamically

6. **Security Implementation**
   - How to ensure security and implement encryption for data protection

## IP Addresses

**Purpose:** Unique identifiers for devices connected to a network.

### IPv4 Addressing

- **Format:** a.b.c.d (dotted decimal notation)
- **Structure:** Each part represents an 8-bit number (range: 0-255)
- **Total Capacity:** Approximately 4.3 billion unique addresses (2³²)
- **Limitation:** Address exhaustion due to internet growth

### IPv6 Addressing

- **Purpose:** Solve IPv4 address exhaustion problem
- **Structure:** 128-bit addresses
- **Capacity:** Vastly expanded address space for future internet growth

## Port Numbers

**Purpose:** Identify specific processes or applications running on a device.

### Port Necessity

- **Problem:** Multiple applications can run simultaneously on a single device
- **Solution:** Port numbers direct incoming data to the correct application
- **Example:** Web servers typically use port 80 for HTTP communication

## Network Architecture Models

### OSI Model (7 Layers)

**Purpose:** Conceptual model for understanding network communication.

**Layer Structure:**

1. **Physical Layer** - Actual data transmission
2. **Data Link Layer** - Direct device communication
3. **Network Layer** - Data routing
4. **Transport Layer** - Reliable data delivery
5. **Session Layer** - Connection management
6. **Presentation Layer** - Data formatting and encryption
7. **Application Layer** - User interface and network services

### TCP/IP Suite (4 Layers)

**Purpose:** Practical, simplified version of the OSI model used in modern internet.

**Layer Structure:**

1. **Link Layer** - Physical and data link functions combined
2. **Internet Layer** - Data routing (equivalent to OSI Network layer)
3. **Transport Layer** - Reliable data delivery
4. **Application Layer** - Combines OSI Application, Presentation, and Session layers

**Key Advantage:** More practical implementation compared to the theoretical OSI model
