# Networks
(check line 348)
A network is a group of connected devices that share data with each other.

## How Computers and Printers Communicate

> When a computer sends data (a bunch of bits) to a printer, for example, does the printer understand what to do?

The communication process involves several key components:

- **Printer Driver:** Printers understand the incoming stream of bits because the computer's printer driver acts as a translator.

  - The printer driver is a piece of software on our computer that enables the computer's operating system to communicate with a piece of hardware. Since the operating system and hardware do not speak the same language, the driver acts as an interpreter.

  - A driver is a set of callbacks/routines that acts as a translator or a bridge between the OS and hardware.

    - **Note:** another word for fucntions

  - The OS only knows how to make generic requests (like "read data" or "send data"), and the driver translates those into highly specific commands that a particular device understands.

  - Its core architecture is as follows:
    1.  **Upper Interface:** Plugs into the OS's kernel and understands a standard set of commands from the OS (like `close`, `read`, `write`).
    2.  **Internal Logic:** The driver's "brain." It takes the generic command from the OS and translates it into the specific sequence of operations that the hardware needs to execute. This logic is unique to each device.
    3.  **Lower Interface:** Communicates directly with the hardware by writing to its registers, sending translated commands through the computer's bus to the device.

- **Driver Internals: I/O Request Packets (IRPs) and Communication**

  - The OS doesn't just send a simple "read" command; it encapsulates the entire operation in a complex data structure called an **I/O Request Packet (IRP)**.

  - **About Packets:**

    - Packets is a unit of data formatted for netwrok transmission
    - Contains both paylaod and a header
      - **Payload:** actual info you are sending
      - **Header:** contains metadata like source and destination ip addressees, port number and error checking info

  - An IRP is a kernel object that contains everything a driver needs to know:

    - **Major and minor function codes:** Specifies the action.
    - **Buffer pointers:** Memory addresses for the data being read from or written to.
    - **Device object:** A pointer to the target device.
    - **Status info.**

  - **Driver Stack:** Devices are managed by a **driver stack**. A single IRP is passed down a chain of drivers.

    - **Stack Architecture:**

      - The term stack is an architectural metaphor for layering and not a literal LIFO data struct
      - Internally OS buidld this stack of device objects using a singly linked list of DEVICE_OBJECT structures
      - Each driver in stack creates a uniq DEVICE_OBJECT to represet a specific device instance in the drivers's perspective
      - Each of these objects contains a pointer to the object of next driver directly below it
      - OS traverses this linked list to passI/O req down the stack

    - **Why Called a Stack:**
      - Its called a stack because the irp is conceptually pushed down through layers and the completion signal travek back up the same path
      - Does not travel up the linked list
      - Higher level drivers can attach a special callback known as completion routine to the irp itself so when a lower driver finishes with the irp the i/o manager sees this routine and executes it giving contol to the higher driver
      - For sync ops higher drivers call to lower driver simple waits for the fucnc to return a status

  - **Example:** For a USB hard drive, IRP might go from:

    1.  **File System driver:** Converts file/byte offsets to logical blocks.
        - **File/byte offsets:** distance from starting point, an integer that indicates position position of somwthing within a larger struct
        - **Logical blocks:** fixed size chunk of data that os uses to view a storage drive and entire drive is seen as a simple numbered sequence of these blocks
    2.  **Volume manager driver:** Manages partitions.
    3.  **USB storage class driver:** Converts block requests to USB storage commands.
        - **Block requests:** request to read/writea fixed-size chunk of data called a block, storage devices like ssd and hdd are called block devices ince they are physically organised to work efficiently with bocks
    4.  **USB host controller driver:** Manages the actual USB protocol.

  - **Device Object Structure for USB Hard Drive:**

    - A single physical USB hard drive exists. To manage it, the OS builds a stack:
    - A Device Object is a data structure in memory that represents an instance of a device from a specific driver's perspective.
    - The File System Driver creates a DEVICE_OBJECT to represent the drive as a "volume with files and folders."
    - It attaches its device object on top of the one below it.
    - The Disk Class Driver creates its own DEVICE_OBJECT to represent the drive as a "sequenc e of logical blocks."
    - It attaches its device object on top of the one below it.
    - The USB Storage Driver creates its DEVICE_OBJECT to represent the drive as a "USB mass storage device."

  - Each driver in the stack processes the IRP, adds its own layer of commands, and passes it to the driver below it.

- **Hardware Controllers: The Middle Management**

  - **What is a Controller:**

    - A controller is a specialized chip or circuit whose job is to manage a subsystem, offloading that specific task from the main CPU.
    - Think of them as middle managers for hardware.
    - The CPU delegates a high-level task (e.g., "save this file"), and the controllers handle the low-level details.

  - Common examples include:
    - **Disk Controller (like SATA or NVMe controllers):** Manages reading from and writing to hard drives or SSDs.
    - **Network Controller:** Manages sending and receiving data packets over a network.
    - **USB Controller:** Manages all devices connected to the USB ports.
    - **DMA Controller:** A special controller whose sole job is to move blocks of data between memory and devices, as explained below.

- **Issuing Commands to Hardware:** Once the IRP reaches the lowest-level driver, it communicates with the physical hardware using two primary techniques that often work together:

  - **Memory-Mapped I/O (MMIO):**

    - The hardware's control registers are mapped to the physical memory address space for hardware comms.
    - The driver writes configuration values directly to these memory addresses, which are routed to the device instead of RAM.
    - This is used to give commands and configure the device.
    - **How it works:**
      - So when like the cpu executes an instruction to write to an address in this reserved range the computer's memory controller knows to send that data to the RAM sticks instead it redirects that command and data across the hardware bus direcly to device's control registers

  - **Direct Memory Access (DMA):**

    - For bulk data transfers where CPU involvement is a bottleneck.
    - The driver first uses MMIO to configure the DMA controller.
    - It tells the controller the source address, destination address, and amount of data to move.
    - The DMA controller then handles the entire transfer between the device and RAM directly.

  - **Summary:**
    - So mmio and dma go hand in hand mmio is for control to write to the device's control registers to set up a task and dma is for bulk data transfer

- **Hardware Interrupts:** When the hardware needs the CPU's attention (e.g., DMA transfer complete, new packet arrived), it sends an **interrupt**. Interrupt handling is split into two phases to ensure the system remains responsive:

  - **Interrupt Request Level (IRQL):**
    - This is a priority system for the CPU.
    - When a hardware interrupt occurs, the CPU's IRQL is raised to the level of that interrupt.
    - While the IRQL is high, any interrupts with a lower or equal priority are ignored (masked).
    - This is why code running at a high IRQL must be extremely fast.

  1.  **Interrupt Service Routine (ISR):** This is the first responder. It runs at a high hardware IRQL (known as DIRQL - Device IRQL), pausing almost all other activity on its CPU core.
      - **How it works:**
        1.  **Context Switch:** The CPU immediately stops its current task, saves its state (the values in its registers), and jumps to the memory address of the ISR, which the driver registered with the OS at startup.
        2.  **Capture Status (MMIO):** The ISR's first action is to read the device's status register using MMIO. This tells the ISR _why_ the device interrupted (e.g., "DMA transfer complete," "Error occurred," "Data ready").
        3.  **Acknowledge Interrupt (MMIO):** It immediately writes to a control register on the device (again, via MMIO) to tell it, "I've received your signal, you can stop sending it now." If this isn't done, the CPU would be stuck in an infinite loop handling the same interrupt.
        4.  **Save Context:** The ISR copies the status it just read, and any other critical, volatile data from the device, into a pre-allocated, non-paged memory area that it shares with the DPC.
        5.  **Queue the DPC:** The ISR calls a kernel function (`KeInsertQueueDpc`), passing it a pointer to a DPC object that was initialized at startup. This tells the OS, "My urgent work is done. Please run this DPC routine as soon as you can to finish the job."
        6.  **Return:** The ISR returns control to the OS, which restores the state of the task that was originally interrupted. This entire process is designed to be over in microseconds.
  2.  **Deferred Procedure Call (DPC):** This is the heavy lifter. It runs shortly after the ISR but at a lower, software-level IRQL (`DISPATCH_LEVEL`). At this level, other, more critical hardware interrupts can still be handled.
      - **How it works:**
        1.  **Execution:** When the CPU's IRQL drops below `DISPATCH_LEVEL`, the OS scheduler checks a queue for the current processor. If it finds the DPC object that the ISR just queued, it executes the DPC function associated with it.
        2.  **Process Data:** The DPC uses the context information saved by the ISR. If it was a read operation, it now copies the data from the hardware's buffer (or the DMA buffer in RAM) into the application's buffer, which was specified in the original IRP.
        3.  **Complete the IRP:** The DPC updates the original I/O Request Packet. It sets the final status (e.g., `STATUS_SUCCESS`) and records how much data was transferred.
        4.  **Notify the OS:** Finally, the DPC calls `IoCompleteRequest`, passing it the completed IRP. This signals the I/O Manager that the entire operation is finished. The I/O Manager then alerts the original application that its requested I/O is done, and its data is ready.

- **Printing Process:**

  - When we click "print," the driver takes the document from our application and converts it into a detailed set of instructions using a **Page Description Language (PDL)** that our printer understands.

  - **Printer driver components:**

    1.  UI component
        - Part we interact with like adjusting settings like papar size etc
        - This gathers preferences and passes then to rendering engine
    2.  Rendering engine (Graphics device interface or GDI)
        - Takes digital doc from application end and with help f driver converts into a format printer can understand

  - **Chain of Command to Print a Document:**

    1.  **Application**

        - Creates a print job by making calls to the gdi

    2.  **GDI Engine**
        - Converts the appplication's drawing commands into an EMF file and calls the print spooler
        - **EMF File (Enhanced Metafile):**
          - A windows vector graphics file
          - **Vector Graphics File:** a graphics file that stores an image as a set of mathematical instructions instead of pixels, same scaling as described below
          - Stores series of drawing commands instead of pixels
          - Since its a set of instructions it is device independent and can be scaled to any size without losing quality
          - This is why the windows print spooler uses EMFs to store print jobs before thyre rendered by the specific driver
    3.  **Print Spooler (spoolsv.exe):**

        - A user mode service
        - **Why User Mode? - Stability and Security:**

          - **Stability Reasons:**

            - If the spooler were in kernel mode, a crash caused by buggy driver or malformed print job could bring down the entire os
            - It crashes the entire os as kernel mode operates in a single shared memory space with hghest cpu privilege level where there are no protective boundaries to contain an error
            - Since in kernel mode all drivers and core os share same virtual address there is no memory isolation like there is for user mode applications

            - **Memory Isolation in User Mode:**

              - The os ensures memory isolation by using hardware and soft ware combination called virtual memory
              - This system tricks each app into believing it has its own private dedicated memory space
              - It has two key components:

                1. **Virtual Address Space:** instead of leftting apps see the real physical ram, os gives each app its own independent linear address space typically startin from zero
                2. **Memory management Unit (MMU):** a piece of hardware on the cpu that acts as a translator when an app tries to access a memory address (virtual)

                   - The mmu ntercepts the request using a set of translation tables called page tables which are maintained by and private to the os
                   - The mmu translates apps virtual into a physical address in the actual ram chips
                   - If an application tries to access a virtual address that does not have a valid tranlation in its page table, mmu hardware triggers a page fault exception
                   - OS catches the fault sees the access is illegal and terminates app generating an acces violation or segmentation fault error

                   - **Stack Overflow and Segmentation Faults:**
                     - This segmentation fault is common you must have seen it during stack overflow in case of recursion this is due to stack over flow being a type of segmentation fault
                     - When os laods your app it dosent give it all of RAM, instead it carves out distinct regions withing the app's virtual address space for diff purposes , one for code, one for global data, one for heap and a relatively small fixed size region for the call stack
                     - During stack overflow function calls occupy the enitre pre allocated stack region
                     - The final step is that the program tries to push oe more stack frame, this pushes stack pointer just beyond the boundary of the memroty region allocated for stack
                     - The program is now attempting to write to a virtual memoty address that was never mapped in its page table mmu hardware instantly detects this attpmt and triggers a page fault

            - **Kernel Mode Risks:**

              - A buggy driver could accidentally write to a wrong memory address and overwrite a critical piece of os code
              - Once a core os structure is corrupted other parts of system will read this bad data and behave unpredictably leading to rapid collapse of system stability
              - Kernel mode also has direct hardware control so a faulty driver can send incorrect commands to a device putting it into an unstable or invalid state from which it cant recover without a full system reset

              - **Unhandled Exceptions at Ring 0:**

                - When an error lie null pointer or divide by zero occurs in user mode app, the os kernel catches the exception

                - **Why OS Catches Exceptions:**

                  - OS catches an exception to handle an error gracefully and prevent program from crashing
                  - If you just leave an exception in a user mode app, the program's default behaviour is to immediately terminate
                  - The os steps in and cleans up

                  - **Cleanup Process:**

                    - Cleaning up means os systematically recalims all the resources that the application was using, it involves:
                      1. **Reclaiming memory:** frreeing all ram both heap and stack that was allocated to the application making it available or other programs
                      2. **Closing handles:** shutting down connections to os resources like open files network sockets and graphics windows
                      3. **Removing kernel structures:** deleting any internal os data structures that were created to manage the applications
                    - OS erases every trace of the terminated app from system's active state ensuring it cant affect other running processes

                  - **Why Cleanup is Critical:**

                    - Because an unhandled error leaves the program in an unkown and unstable state continuing to run would lead to incorrect behaviour corrupeted data or security vulnerabilties

                    - **Security Vulnerabilities if Cleanup Failed:**
                      1. **Information disclosure:** memory that the crashed app was using would not be wiped, next app gets same allocated block of ram could read the leftover data, could expose sensitive info like passwords encryption keys etc
                      2. **Use after free exploits:** if os didnt properly invalidate pointers or handles, a malicious program could try to reuse these dangling handles
                         - **What is a Handle:** a handle is a abstract reference that our app uses to interact with a resource managed by the os, whne app opens a file for example, os creates the resource in kernel and gives your app back ahandle which is essentially a uniq number, app never gets a direct memory poiner only holds the ticket
                         - Like a handle might have pointed to a file with high privileges, a new malicious file could use it to gain unauthorized acces to that file
                      3. **Resource exhaustion:** if memory and handles werent reclaimed they would be lost forever until next reboot, a maliciious actor could repeatedly crash a program to deliberately leak resources eventually consuming all available memory or handles and causing the entire system to fail (a DOS)

                - **Kernel Mode Exception Handling:**

                  - Terminates the single misbehaving application and cleans up its resources, when the same error happens in kernel mode there is no higher authority to catch it
                  - Since kernel itself is now in an unkown and untrustworthy state, it cant be allowed to continue
                  - The cpu's exception handlin mechanism will transfer control to a special os routine whose only safe option is to halt the system a process known as kernel panic or in windows a bug check that generates the blue screen of death
                  - When the supervisor, kernel, fails the whole system fails as thers nothing left to supervise it

                  - **How OS Catches Exceptions:**
                    - The os catches exceptions using a hardware level mechanism
                    - When an error occurs the cpu hardware itself automatically stops what its doin and transfers control to a pre registered exception handler fucntion within the os kernel
                    - Process is similar to how cpu hndles hardware interrupts
                    - CPU detects errors as its hardwired into the processor's design and not a software check
                    - The alu has a circuitry that physically detects impossible math, the mmu detects page faults, the instruction decoder recognizs when its fed a a sequence of bits that dont correspond to any valid cpu instruction

          - **Security Reasons:**
            - The spooler handles network connection and parses complex files, making it a target for attacks
            - Running it in the user mode creates a critical security boundary preventing vulnerabilities from compromising the os kernel

        - **Spooler Functions:**

          - That manages print queues, it stores the emf file and schedules the job
          - When its time to print it loads the appropriate printer driver
          - The spooler dosent directly touch the kernel-mode drivers, it uses a middle man called port monitor

          - **Port Monitor Example:** usbmon.dll for usb

            - **What is a .dll file:**
              - .dll file is a dynamic link library which is microsoft's implementation of a shared library in windows
              - Its a file containingcode and data that can be used by multiple programs simultaneously
              - When a program needs to perform a certain function instead of having the code for that func built directly into its own .exe file, it contains a reference that says, go find the func i need in shared_library.dll
              - When you run the program, windows loader find s the required dlls, loads them into memory and connects the program to the fucntions it needs
              - This is called dynamic linking as linking happens at run time not when program is compiled
              - It saves a significant amount of ram since multiple running programs can use the exact sam copy of DLL thats loaded into meomry
              - Devs can put common funcs into a dll and reuse them accross many diff apps
              - You can update or fix a bug in a func by just replacing dll filewithou having to recompile and redistribute every app that uses it
              - C and cpp are the most used languages for dlls

          - **The Handoff Process:**
            - After the user mode driver renders the print job into a lang like pcl the spooler gives this final data to the port monitor
            - The port monitor makes a std sys call to send to the kernel device that represents the physical port
            - This sys call is the official bridge to the kernel, it triggers the I?O manger to create an iRP and sends it to the top of the kernel mode driver stack which delivers the data to the hardware

    4.  **Printer Driver (user mode components)**

        1. **Graphics driver:** a core microsoft driver like UNIDRV.dll (for PCL) or PSCRIPT5.dll (for postscript) it does the heavy liftig of converting emf file's commands into the printer sepcific PDL
        2. **Configuration module:** the manufacturer specific part that tells the graphics driver about the printer's unique features

    5.  **Port Monitor (e.g.usbmon.dll)**

        - A user mode dll responsible for taking the final rendered data (the pcl or postscript code) and sending it to the correct kernel mode driver
        - Its the bridge to the kernel

    6.  **Bus driver (kernel mode)**
        - Final low level driver stack

  - **Print Job Data Flow:**

    - Here's how a print job flows though the above stack showing how the request is transformed at each layer:

    - **Stage 1: User Initiation**

      - A user clicks print in an app, the request to write the doc to the printer begins a multi stage journey

    - **Stage 2: GDI Processing**

      - The initial request isnt a single I/O request packet (IRP) but a series of GDI function calls
      - These calls are processed by the gdi engine which creates an emf file and psses the job to the print spooler
      - The spooler then takes over callling the specific printer driver to render the emf into a final data stream

    - **Stage 3: Transition to Kernel**

      - Atp, the request is ready to transition to the kernel
      - The port monitor takes the rendered pcl data and issues a series of writefile() commands
      - These commands are what the os turns into IRPs

    - **Stage 4: Kernel Processing**
      - These IRPs containing chunks of the PCL data are handed to the top of the kernel mode bus stack
      - For a usb printer the irp travels down the chain from usb port driver which manages the logical connection to the usb hub driver and finally to the usb host controller driver
      - This lowest level driver translates irp's write data command into the actual electrical signals sent over the usb cable to the printer completeing the operation

---

## Does every piece of information sent by the computer have to be printed by the printer?

No, a significant portion of data sent to a printer consists of non printable control commands and transport protocol overhead, not just the content to be printed, the data stream is interpreted not just blindly outputted

- **Data Stream Structure:**

  - Data sent from computer to the printer is structured stream defined by PDL
  - This stream contains 2 distinct types of info:
    1. **Control commands (metadata):** these are instructions that configure the printer's state and manage the print job, they are not rendered on the page, examples include page size, selecting paper tray etc
    2. **Renderable data (payload):** actual content, vector graphics commands, text character codes and raster image bitmaps that will be processed and transfered onto the page

- **Page Description Language (PDL):**

  - This language includes commands for setting margins, selecting fonts, drawing complex graphics, and more.

- **Raster Image Processor (RIP):**

  - The printer has a built-in processor called a **Raster Image Processor (RIP)** that reads these PDL commands and translates them into tiny pixels that form the final image on paper.

  - **RIP Processing:**

    - When it encounters a control command, it modifies the printer's internal state variable
    - When it encounters readable data, it executes drawing commands to create a digital bitmap of the page in the printer's memory (rasterization)
    - Once the entire page is rasterized in memory, the RIP signals the physical print engine to transfer this bitmap onto the paper
    - **Raster image:** or raster image is a grip of pixels that represents an image, image is broken down into a grip of pixels, color of each individual pixel is represnted by a certain number of bits

  - **Transport Protocol Overhead:**
    - Before the PDL data is even sent, its encapsulated in lower level transport protocols
    - If its a network printer, the entire pdl stream is broken down into thousands of TCP/IP packets
    - Each packet is wrapped with TCP and IP headers containing source/destination addresses, port numbers and sequence information
    - This data is essential for transport but is stripped away by the printer's network interface and is never seen by the RIP
    - The same principle applies to USB packets for a local printer


# Actual important stuff starts from here


# Network Communication Fundamentals

## Protocol Definition and Necessity

**Question:** Will the printer automatically know that the first 20 bytes are metadata and the next 80 bytes are what I have to print?

**Answer:** No. Just as humans must understand the language being spoken before they can communicate effectively, devices require established communication rules before they can exchange information. These rules are called **protocols**.

### Protocol Overview

- **Protocol Definition:**

  - A set of standardized rules that enable devices to communicate with each other
  - Encompasses format, timing, sequencing, and error control mechanisms

- **Protocol Categories:**
  - **Physical Protocols:** Define electrical and mechanical aspects of communication
  - **Logical/Software Protocols:** Define data format, message structure, and communication procedures

## Network Communication Challenges

Network communications involve significant complexity, requiring multiple specialized protocols to address challenges at each communication layer. To understand this complexity, consider the fundamental problems that must be solved.

### Scenario Analysis: Browser-to-Server Communication

**Example:** When a user types "google.com" in their browser, a request travels to Google's server and returns a response. This seemingly simple operation involves solving numerous complex problems.

### The Eighteen Fundamental Network Problems

#### 1. Address Resolution

- **Challenge:** How does the browser determine the server's network address?
- **Context:** Domain names must be translated to IP addresses

#### 2. Server Selection

- **Challenge:** When multiple servers exist, how does the browser determine the appropriate destination?
- **Context:** Load balancing and server farm management

#### 3. Request Authentication

- **Challenge:** How does the server identify the request sender?
- **Context:** Client identification and access control

#### 4. Client Address Discovery

- **Challenge:** How does the server determine the client's return address?
- **Context:** Response routing and bidirectional communication

#### 5. Global Server Identification

- **Challenge:** With millions of servers worldwide, how is each uniquely identified?
- **Context:** Hierarchical addressing and namespace management

#### 6. Route Discovery

- **Challenge:** Given a known address, how is the optimal path determined?
- **Context:** Network topology and routing algorithms

#### 7. Path Optimization

- **Challenge:** In a mesh network spanning continents, how is the best path calculated?
- **Context:** Graph theory application in network routing

#### 8. Dynamic Path Selection

- **Challenge:** What constitutes the "shortest path" - hop count or performance metrics?
- **Context:** Load balancing and congestion avoidance

#### 9. Network State Monitoring

- **Challenge:** How do network devices track real-time congestion and availability?
- **Context:** Distributed state management and telemetry

#### 10. Data Segmentation Strategy

- **Challenge:** Should large data (e.g., 10MB) be transmitted as a single chunk?
- **Context:** Bandwidth sharing and network fairness

#### 11. Packet Independence

- **Challenge:** How do individual packets navigate independently to their destination?
- **Context:** Packet-switched networking and metadata requirements

#### 12. Metadata Efficiency

- **Challenge:** How much metadata should each packet contain, and how is redundancy minimized?
- **Context:** Protocol overhead vs. functionality trade-offs

#### 13. Packet Loss Detection

- **Challenge:** How are lost or corrupted packets identified during transmission?
- **Context:** Electrical interference and connection failures

#### 14. Data Integrity Verification

- **Challenge:** How does the receiver detect corrupted data (e.g., "10" received as "01")?
- **Context:** Error detection mechanisms and checksums

#### 15. Error Message Reliability

- **Challenge:** What happens when error correction messages themselves become corrupted?
- **Context:** Recursive reliability problems

#### 16. Dynamic Route Recovery

- **Challenge:** How do network devices detect and respond to path failures?
- **Context:** Network resilience and fault tolerance

#### 17. Data Privacy

- **Challenge:** How is transmitted data protected from unauthorized access at intermediate nodes?
- **Context:** Network security and eavesdropping prevention

#### 18. Secure Key Exchange

- **Challenge:** How are encryption keys safely distributed without compromising security?
- **Context:** Cryptographic key management and distribution

### Fundamental Network Principle

**Key Insight:** Every solution to a network problem introduces new challenges, creating a complex ecosystem of interdependent protocols and mechanisms.

# Network Addressing Architecture

## The Unique Identification Problem

**Core Question:** How do we uniquely identify each server on the internet?

**Solution Approach:** When faced with any unique identification challenge, the standard solution is implementing a unique identifier system.

## Internet Protocol (IP) Addressing

### IP Address Fundamentals

- **Definition:** A unique identifier assigned to each device connected to a network
- **Purpose:** Enables precise routing of data across global networks
- **Analogy:** Functions similarly to postal addresses in physical mail systems

### IPv4 Address Structure

- **Format:** Dotted decimal notation (a.b.c.d)
  - Each segment (a, b, c, d) represents an 8-bit number (0-255)
  - **Total Address Space:** 2³² = 4.3 billion possible addresses
  - **Limitation:** Address exhaustion due to internet growth

### IPv6 Address Evolution

- **Motivation:** IPv4 address space depletion
- **Format:** 128-bit addressing scheme
- **Capacity:** Vastly expanded address space (2¹²⁸ addresses)

### IPv4-IPv6 Transition Challenges

- **Scenario:** During the transition period, compatibility issues arose
  - **Server Side:** Google and other major services adopted IPv6
  - **Client Side:** ISPs like Airtel maintained IPv4 infrastructure due to upgrade costs
- **Problem:** How do IPv4 clients communicate with IPv6 servers?
- **Solution:** Public and private network architectures (detailed in subsequent classes)

## Port-Based Process Identification

### The Application Routing Problem

**Question:** Is device identification sufficient for data transfer?

**Analysis:** While IP addresses identify devices, modern systems run multiple applications simultaneously. The operating system must route incoming data to the appropriate application or process.

### Port Number System

- **Definition:** A unique identifier for a specific process or service on a device
- **Function:** Enables multiplexing of network connections on a single device
- **Range:** 16-bit numbers (0-65535)

### Port Number Examples

- **Standard HTTP:** google.com:80
  - Port 80 is the default HTTP port
  - Browser successfully connects and loads content
- **Non-standard Port:** google.com:81
  - Connection fails because Google doesn't provide HTTP service on port 81
  - Demonstrates port-specific service binding

### Frontend vs. Backend Port Binding

**Question:** Why do we bind backend services to ports but not frontend applications?

**Answer:** This concept is addressed in detail during the second class of the networking curriculum.

# Network Architecture Models

## Historical Development

### Early Internet Evolution

The modern internet evolved from academic networks:

- **Origin:** Universities in the United States operated independent networks
- **Expansion:** Decision to interconnect these networks led to the World Wide Web
- **Complexity Challenge:** As the internet grew, management became increasingly complex

### OSI Model Development

- **Timeline:** Developed during the 1970s and 1980s
- **Purpose:** Open Systems Interconnection (OSI) model simplified internet complexity
- **Approach:** Decomposed networking into manageable, specialized layers
- **Design Philosophy:** Created modular architecture to accommodate future technological evolution

## OSI Reference Model

### Seven-Layer Architecture

The OSI model consists of seven conceptual layers, each with specific responsibilities:

#### Layer 7: Application Layer

- **Purpose:** Provide network services directly to end-user applications
- **Primary Protocol:** HTTP (Hypertext Transfer Protocol)
- **Function:** Interface between user applications and network services

#### Layer 6: Presentation Layer

- **Purpose:** Handle data encryption, compression, and formatting
- **Primary Protocol:** SSL/TLS (Secure Sockets Layer/Transport Layer Security)
- **Function:** Data translation and security services

#### Layer 5: Session Layer

- **Purpose:** Manage communication sessions between devices
- **Definition:** Controls the entire conversation lifecycle, including authentication and state management
- **Implementation:** Includes mechanisms like cookies and authentication tokens
- **Note:** While session management appears in application code, OSI treats it as a separate conceptual layer

#### Layer 4: Transport Layer

- **Importance:** Critical layer requiring extensive study
- **Purpose:** Ensure reliable data delivery between endpoints
- **Primary Protocol:** TCP (Transmission Control Protocol)
- **Function:** Error detection, correction, and flow control

#### Layer 3: Network Layer

- **Importance:** Fundamental to internet operation
- **Purpose:** Route data efficiently across network infrastructure
- **Components:** IP protocol, routing algorithms, router functionality
- **Function:** Path determination and logical addressing

#### Layer 2: Data Link Layer

- **Purpose:** Manage communication between directly connected devices
- **Primary Addressing:** MAC (Media Access Control) addresses
- **Function:** Frame formatting and local network error detection

#### Layer 1: Physical Layer

- **Purpose:** Handle actual data transmission over physical media
- **Function:** Electrical, optical, and radio signal management

## TCP/IP Protocol Suite

### Simplified Network Model

The TCP/IP model represents a more practical approach to network architecture:

- **Philosophy:** Simplified version of OSI model
- **Adoption:** Modern internet standard
- **Structure:** Four-layer architecture

### TCP/IP Layer Structure

#### Application Layer

- **Scope:** Combines OSI layers 5, 6, and 7
- **Rationale:** Application, presentation, and session functions don't require independent layers in practice

#### Transport Layer

- **Function:** Equivalent to OSI Layer 4
- **Protocols:** TCP, UDP

#### Internet Layer

- **Function:** Renamed from "Network Layer"
- **Protocols:** IP, ICMP, routing protocols

#### Link Layer

- **Function:** Combines OSI physical and data link layers
- **Rationale:** Physical and data link functions are closely integrated in implementation
