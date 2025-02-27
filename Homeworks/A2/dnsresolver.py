import dns.message
import dns.query
import dns.rdatatype
import dns.resolver
import time

# Root DNS servers used to start the iterative resolution process
ROOT_SERVERS = {
    "198.41.0.4": "Root (a.root-servers.net)",
    "199.9.14.201": "Root (b.root-servers.net)",
    "192.33.4.12": "Root (c.root-servers.net)",
    "199.7.91.13": "Root (d.root-servers.net)",
    "192.203.230.10": "Root (e.root-servers.net)"
}

TIMEOUT = 3  # Timeout in seconds for each DNS query attempt

def send_dns_query(server, domain):
    """ 
    Sends a DNS query to the given server for an A record of the specified domain.
    Returns the response if successful, otherwise returns None.
    """
    try:
        query = dns.message.make_query(domain, dns.rdatatype.A)  # Construct the DNS query
        # TODO: Send the query using UDP 
        # Note that above TODO can be just a return statement with the UDP query!
        """
        EXPLANATION:
        Enable EDNS with a 4096-byte UDP buffer (increases response capacity)
        This increases the response capacity and may improve performance when resolving large domains
        And, it will contain the ip addresses(in response.additional field) of all the domains provided in response.authority field.
        If this line is not included, all the ip addresses of NS name severs are not recieved in the response.additional field.
        """
        query.use_edns(0, payload=4096)
        """
        EXPLANATION:
        Then, this function will make a query to given server(IP address) with query msg within the timout window.
        response will be none if some error occured (like timeout).
        """
        response = dns.query.udp(query, server, timeout=TIMEOUT)
        return response  # Return the response if successful
    except Exception:
        return None  # If an error occurs (timeout, unreachable server, etc.), return None

def extract_next_nameservers(response):
    """ 
    Extracts nameserver (NS) records from the authority section of the response.
    Then, resolves those NS names to IP addresses.
    Returns a list of IPs of the next authoritative nameservers.
    """
    ns_ips = []  # List to store resolved nameserver IPs
    ns_names = []  # List to store nameserver domain names
    
    # Loop through the authority section to extract NS records
    for rrset in response.authority:
        if rrset.rdtype == dns.rdatatype.NS:
            for rr in rrset:
                ns_name = rr.to_text()
                ns_names.append(ns_name)  # Extract nameserver hostname
                print(f"Extracted NS hostname: {ns_name}")
    # TODO: Resolve the extracted NS hostnames to IP addresses
    # To TODO, you would have to write a similar loop as above
    """
    EXPLANATION:
    Match extracted NS hostnames with IP addresses from the additional section
    We can extract the IP addresses of all the name servers provided in authority field from the additional section of the response.
    We have increased the UDP msg size to 4096 bytes from 512 bytes (refer to send dns_query function),
    since all the IP addresses were not sent in additional field if default size is used.
    """
    for rrset in response.additional:
        if rrset.rdtype == dns.rdatatype.A:
            for rr in rrset:
                if rrset.name.to_text() in ns_names:
                    ns_ips.append(rr.address)
                    print(f"Resolved {rrset.name.to_text()} to {rr.address}")

    """Used for debugging"""
    # print(f"Number of NS records: {ns_names.__len__()}")
    # print(f"Number of NS records resolved: {ns_ips.__len__()}")
    
    return ns_ips  # Return list of resolved nameserver IPs

def iterative_dns_lookup(domain):
    """ 
    Performs an iterative DNS resolution starting from root servers.
    It queries root servers, then TLD servers, then authoritative servers,
    following the hierarchy until an answer is found or resolution fails.
    """
    print(f"[Iterative DNS Lookup] Resolving {domain}")

    next_ns_list = list(ROOT_SERVERS.keys())  # Start with the root server IPs
    stage = "ROOT"  # Track resolution stage (ROOT, TLD, AUTH)

    while next_ns_list:
        ns_ip = next_ns_list.pop(0)  # Pick the first available nameserver to query
        response = send_dns_query(ns_ip, domain)
        
        if response: #checks if response is not NONE
            print(f"[DEBUG] Querying {stage} server ({ns_ip}) - SUCCESS")
            
            # If an answer is found, print and return
            if response.answer:
                print(f"[SUCCESS] {domain} -> {response.answer[0][0]}")
                return
            
            # If no answer, extract the next set of nameservers
            next_ns_list = extract_next_nameservers(response)
            # TODO: Move to the next resolution stage, i.e., it is either TLD, ROOT, or AUTH
            """
            EXPLANATION:
            After successfully resolving the nameserver,
            we need to move to the next stage.
            If we are in the ROOT stage, we move to the TLD stage.
            If we are in the TLD stage, we move to the AUTH stage.
            This way, we continue to the next stage until we either find an answer or reach the end of the resolution chain.
            """
            if stage == "ROOT":
                stage = "TLD"  # Move to TLD stage after querying ROOT servers
            elif stage == "TLD":
                stage = "AUTH"  # Move to AUTH stage after querying TLD servers

        else:
            print(f"[ERROR] Query failed for {stage} {ns_ip}")
            # return  # Stop resolution if a query fails
    
    print("[ERROR] Resolution failed.")  # Final failure message if no nameservers respond

def recursive_dns_lookup(domain):
    """ 
    Performs recursive DNS resolution using the system's default resolver.
    This approach relies on a resolver (like Google DNS or a local ISP resolver)
    to fetch the result recursively.
    """
    print(f"[Recursive DNS Lookup] Resolving {domain}")
    try:
        # TODO: Perform recursive resolution using the system's DNS resolver
        # Notice that the next line is looping through, therefore you should have something like answer = ??
        """
        EXPLANATION:
        Since the loop provided is using answer, we need to populate it with "NS" name server's names and ip addresses.
        That can be achieved by using resolver function with "NS" as parameter with the same domain.
        """
        answer = dns.resolver.resolve(domain, "NS")
        for rdata in answer:
            print(f"[SUCCESS] {domain} -> {rdata}")

        answer = dns.resolver.resolve(domain, "A")
        for rdata in answer:
            print(f"[SUCCESS] {domain} -> {rdata}")
    except Exception as e:
        print(f"[ERROR] Recursive lookup failed: {e}")  # Handle resolution failure

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3 or sys.argv[1] not in {"iterative", "recursive"}:
        print("Usage: python3 dns_server.py <iterative|recursive> <domain>")
        sys.exit(1)

    mode = sys.argv[1]  # Get mode (iterative or recursive)
    domain = sys.argv[2]  # Get domain to resolve
    start_time = time.time()  # Record start time
    
    # Execute the selected DNS resolution mode
    if mode == "iterative":
        iterative_dns_lookup(domain)
    else:
        recursive_dns_lookup(domain)
    
    print(f"Time taken: {time.time() - start_time:.3f} seconds")  # Print execution time
