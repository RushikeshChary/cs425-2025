# TCP Three-Way Handshake Implementation

## Overview
This project implements the TCP three-way handshake protocol using raw sockets in C++. The implementation provides a client-server model where the client initiates the connection by sending a SYN packet, the server responds with a SYN-ACK packet, and the client completes the handshake with an ACK packet. This fundamental networking concept is implemented at a low level, providing insight into the mechanics of TCP connection establishment.

## Features
- Complete implementation of TCP three-way handshake protocol
- Raw socket programming for direct packet manipulation
- Custom IP and TCP header construction
- Predefined sequence numbers for clarity
- Detailed logging of packet flags and connection status
- Proper error handling and socket management

## Usage

### Prerequisites
- Linux-based operating system
- Root/administrator privileges (required for raw sockets)
- GCC/G++ compiler

### Compilation
```bash
g++ -o server server.cpp
g++ -o client client.cpp
```

### Running the Programs
1. First, start the server (requires root privileges):
```bash
sudo ./server
```
2. Then, in a separate terminal, run the client (requires root privileges):
```bash
sudo ./client
```
### Example Run

Server Output:
```bash
[+] Server listening on port 12345...
[+] TCP Flags: SYN: 1 ACK: 0 FIN: 0 RST: 0 PSH: 0 SEQ: 200
[+] Received SYN from 127.0.0.1
[+] Sent SYN-ACK
[+] TCP Flags: SYN: 0 ACK: 1 FIN: 0 RST: 0 PSH: 0 SEQ: 600
[+] Received ACK, handshake complete.
```

Client Output:
```bash
[+] Starting TCP three-way handshake client...
[+] Sent SYN packet with sequence number 200
[+] TCP Flags: SYN: 1 ACK: 1 FIN: 0 RST: 0 PSH: 0 SEQ: 400
[+] Received SYN-ACK from 127.0.0.1
[+] Sent ACK packet with sequence number 600
[+] TCP three-way handshake completed successfully!
```

## Explanation of client.cpp

The client implementation consists of three main components:

1. **SYN Packet Construction and Transmission**: (send_syn() function)
   - Creates a raw socket with IP header inclusion
   - Constructs a TCP packet with the SYN flag set
   - Sets the initial sequence number to 200
   - Transmits the packet to the server (127.0.0.1:12345)

2. **SYN-ACK Reception**: (Part of perform_handshake() function)
   - Listens for incoming packets on the raw socket
   - Filters packets based on source/destination ports
   - Validates TCP flags (SYN=1, ACK=1)
   - Confirms the server's sequence number (400) and acknowledgment number (201)

3. **ACK Packet Transmission**: (send_ack() function)
   - Constructs the final ACK packet with sequence number 600
   - Sets the acknowledgment number to 401 (server's sequence + 1)
   - Transmits the packet to complete the handshake

The client uses proper error handling and filtering to ensure only relevant packets are processed during the handshake procedure.

## Challenges Faced

1. **Raw Socket Permissions**: Raw sockets require root privileges, which can create complications in some environments.

2. **Packet Filtering**: Properly filtering received packets was challenging, as the socket receives all TCP packets on the system.

3. **Header Structure**: Correctly populating IP and TCP headers required careful attention to byte ordering (network vs. host).

4. **IP and TCP Flags**: Understanding and correctly setting the various header flags was crucial for successful implementation.

5. **Debugging Transport Layer Issues**: With no standardized error messages for raw packets, debugging required extensive packet inspection.

## References

1. RFC 793: Transmission Control Protocol - [https://tools.ietf.org/html/rfc793](https://tools.ietf.org/html/rfc793)

2. W. Richard Stevens, "TCP/IP Illustrated, Volume 1: The Protocols"

3. Linux Socket Programming by Example - Warren Gay

4. Linux man pages:
   - socket(2)
   - setsockopt(2)
   - sendto(2)
   - recvfrom(2)

5. netinet/ip.h and netinet/tcp.h header documentation

## Declaration

We declare that this implementation is our own work and does not involve plagiarism.