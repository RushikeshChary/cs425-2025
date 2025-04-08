#include <iostream>
#include <cstring>
#include <cstdlib>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_PORT 12345
#define CLIENT_PORT 54321

void print_tcp_flags(struct tcphdr *tcp) {
    std::cout << "[+] TCP Flags: "
              << " SYN: " << tcp->syn
              << " ACK: " << tcp->ack
              << " FIN: " << tcp->fin
              << " RST: " << tcp->rst
              << " PSH: " << tcp->psh
              << " SEQ: " << ntohl(tcp->seq) << std::endl;
}

void send_syn(int sock) {
    char packet[sizeof(struct iphdr) + sizeof(struct tcphdr)];
    memset(packet, 0, sizeof(packet));

    struct iphdr *ip = (struct iphdr *)packet;
    struct tcphdr *tcp = (struct tcphdr *)(packet + sizeof(struct iphdr));

    // Fill IP header
    ip->ihl = 5;
    ip->version = 4;
    ip->tos = 0;
    ip->tot_len = htons(sizeof(packet));
    ip->id = htons(12345);
    ip->frag_off = 0;
    ip->ttl = 64;
    ip->protocol = IPPROTO_TCP;
    ip->saddr = inet_addr("127.0.0.1");  // Client address
    ip->daddr = inet_addr("127.0.0.1");  // Server address

    // Fill TCP header
    tcp->source = htons(CLIENT_PORT);
    tcp->dest = htons(SERVER_PORT);
    tcp->seq = htonl(200);  // Initial sequence number as required
    tcp->ack_seq = 0;
    tcp->doff = 5;
    tcp->syn = 1;  // SYN flag
    tcp->window = htons(8192);
    tcp->check = 0;  // Kernel will compute the checksum

    struct sockaddr_in dest_addr;
    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(SERVER_PORT);
    dest_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Send SYN packet
    if (sendto(sock, packet, sizeof(packet), 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr)) < 0) {
        perror("sendto() failed");
        exit(EXIT_FAILURE);
    } else {
        std::cout << "[+] Sent SYN packet with sequence number 200" << std::endl;
    }
}

void send_ack(int sock) {
    char packet[sizeof(struct iphdr) + sizeof(struct tcphdr)];
    memset(packet, 0, sizeof(packet));

    struct iphdr *ip = (struct iphdr *)packet;
    struct tcphdr *tcp = (struct tcphdr *)(packet + sizeof(struct iphdr));

    // Fill IP header
    ip->ihl = 5;
    ip->version = 4;
    ip->tos = 0;
    ip->tot_len = htons(sizeof(packet));
    ip->id = htons(12346);
    ip->frag_off = 0;
    ip->ttl = 64;
    ip->protocol = IPPROTO_TCP;
    ip->saddr = inet_addr("127.0.0.1");  // Client address
    ip->daddr = inet_addr("127.0.0.1");  // Server address

    // Fill TCP header
    tcp->source = htons(CLIENT_PORT);
    tcp->dest = htons(SERVER_PORT);
    tcp->seq = htonl(600);  // Final sequence number as required
    tcp->ack_seq = htonl(401);  // Acknowledging server's sequence number + 1
    tcp->doff = 5;
    tcp->ack = 1;  // ACK flag
    tcp->window = htons(8192);
    tcp->check = 0;  // Kernel will compute the checksum

    struct sockaddr_in dest_addr;
    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(SERVER_PORT);
    dest_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Send ACK packet
    if (sendto(sock, packet, sizeof(packet), 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr)) < 0) {
        perror("sendto() failed");
        exit(EXIT_FAILURE);
    } else {
        std::cout << "[+] Sent ACK packet with sequence number 600" << std::endl;
    }
}

void perform_handshake() {
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sock < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Enable IP header inclusion
    int one = 1;
    if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one)) < 0) {
        perror("setsockopt() failed");
        exit(EXIT_FAILURE);
    }

    // Step 1: Send SYN packet
    send_syn(sock);

    // Step 2: Receive SYN-ACK
    char buffer[65536];
    struct sockaddr_in source_addr;
    socklen_t addr_len = sizeof(source_addr);
    bool syn_ack_received = false;

    while (!syn_ack_received) {
        int data_size = recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr *)&source_addr, &addr_len);
        if (data_size < 0) {
            perror("Packet reception failed");
            continue;
        }

        struct iphdr *ip = (struct iphdr *)buffer;
        struct tcphdr *tcp = (struct tcphdr *)(buffer + (ip->ihl * 4));

        // Filter for packets from the server to our client port
        if (ntohs(tcp->dest) != CLIENT_PORT || ntohs(tcp->source) != SERVER_PORT) {
            continue;
        }

        print_tcp_flags(tcp);

        // Check if this is a SYN-ACK packet with the expected sequence numbers
        if (tcp->syn == 1 && tcp->ack == 1 && 
            ntohl(tcp->seq) == 400 && ntohl(tcp->ack_seq) == 201) {
            std::cout << "[+] Received SYN-ACK from " << inet_ntoa(source_addr.sin_addr) << std::endl;
            syn_ack_received = true;

            // Step 3: Send ACK to complete handshake
            send_ack(sock);
            std::cout << "[+] TCP three-way handshake completed successfully!" << std::endl;
        }
    }

    close(sock);
}

int main() {
    std::cout << "[+] Starting TCP three-way handshake client..." << std::endl;
    perform_handshake();
    return 0;
}
