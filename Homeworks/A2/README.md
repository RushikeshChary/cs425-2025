# DNS Resolver README

This project implements a DNS resolver that supports both **iterative** and **recursive** DNS lookups.

## Overview

The DNS resolver script allows you to:
- Perform **iterative DNS resolution** by querying root servers, TLD servers, and authoritative servers.
- Perform **recursive DNS resolution** using the python dns library's DNS resolver.

## Features
- Supports both iterative and recursive DNS lookups
- Displays detailed logs of the resolution process
- Provides time taken for DNS resolution

## Usage
Ensure denpendencies are installed:
```bash
pip install -r requirements.txt
```
Run the script with the following command:

```bash
python dnsresolver.py <mode> <domain>
```

### Parameters
- `<mode>`: `iterative` or `recursive`
- `<domain>`: The domain name you want to resolve

### Examples

#### Iterative DNS Lookup

```bash
python3 dnsresolver.py iterative google.com

[ Iterative DNS Lookup ] Resolving google . com
[ DEBUG ] Querying ROOT server (198.41.0.4) - SUCCESS
Extracted NS hostname : l.gtld-servers.net.
Extracted NS hostname : j.gtld-servers.net.
Extracted NS hostname : h.gtld-servers.net.
Extracted NS hostname : d.gtld-servers.net.
Extracted NS hostname : b.gtld-servers.net.
Extracted NS hostname : f.gtld-servers.net.
Extracted NS hostname : k.gtld-servers.net.
Extracted NS hostname : m.gtld-servers.net.
Extracted NS hostname : i.gtld-servers.net.
Extracted NS hostname : g.gtld-servers.net.
Extracted NS hostname : a.gtld-servers.net.
Extracted NS hostname : c.gtld-servers.net.
Extracted NS hostname : e.gtld-servers.net.
Resolved l.gtld-servers.net. to 192.41.162.30
Resolved j.gtld-servers.net. to 192.48.79.30
Resolved h.gtld-servers.net. to 192.54.112.30
Resolved d.gtld-servers.net. to 192.31.80.30
Resolved b.gtld-servers.net. to 192.33.14.30
Resolved f.gtld-servers.net. to 192.35.51.30
Resolved k.gtld-servers.net. to 192.52.178.30
Resolved m.gtld-servers.net. to 192.55.83.30
Resolved i.gtld-servers.net. to 192.43.172.30
Resolved g.gtld-servers.net. to 192.42.93.30
Resolved a.gtld-servers.net. to 192.5.6.30
Resolved c.gtld-servers.net. to 192.26.92.30
Resolved e.gtld-servers.net. to 192.12.94.30
[ DEBUG ] Querying TLD server (192.41.162.30) - SUCCESS
Extracted NS hostname : ns2.google.com.
Extracted NS hostname : ns1.google.com.
Extracted NS hostname : ns3.google.com.
Extracted NS hostname : ns4.google.com.
Resolved ns2.google.com. to 216.239.34.10
Resolved ns1.google.com. to 216.239.32.10
Resolved ns3.google.com. to 216.239.36.10
Resolved ns4.google.com. to 216.239.38.10
[ DEBUG ] Querying AUTH server (216.239.34.10) - SUCCESS
[ SUCCESS ] google . com -> 142.250.194.78
Time taken : 0.654 seconds
```

#### Recursive DNS Lookup

```bash
python3 dnsresolver.py recursive google.com

[ Recursive DNS Lookup ] Resolving google.com
[ SUCCESS ] google.com -> ns4.google.com.
[ SUCCESS ] google.com -> ns3.google.com.
[ SUCCESS ] google.com -> ns2.google.com.
[ SUCCESS ] google.com -> ns1.google.com.
[ SUCCESS ] google.com -> 172.217.167.206
Time taken : 0.016 seconds
```

## Explanation of TODO Sections

### 1. Sending a DNS Query (send_dns_query function)

#### TODO: Send the query using UDP

In this section, the script constructs a DNS query for an **A record** and sends it via UDP using the `dns.query.udp()` method.

#### Explanation:
1. **EDNS (Extension Mechanisms for DNS)** is enabled with a buffer size of **4096 bytes** to handle larger DNS responses.
   - This ensures we receive **IP addresses** of all nameservers in the `response.additional` section.
2. If the query succeeds, the function returns the **DNS response**.
3. If an error occurs (e.g., timeout), it returns `None`.

### 2. Extracting Next Nameservers (extract_next_nameservers function)

#### TODO: Resolve the extracted NS hostnames to IP addresses

This section resolves the **NS records** (nameserver domain names) to their corresponding **IP addresses**.

#### Explanation:
1. The function first extracts **NS records** from the **authority section**.
2. It then matches these records with the **IP addresses** found in the **additional section**.
3. The increased UDP buffer size (4096 bytes) ensures that all IPs are included in the additional section.

### 3. Handling DNS Resolution Stages (iterative_dns_lookup function)

#### TODO: Move to the next resolution stage (ROOT, TLD, AUTH)

As the script iterates through nameservers, it tracks the **DNS resolution stage**.

#### Explanation:
1. Starts with **root servers** (ROOT stage).
2. Moves to **TLD servers** after root servers respond.
3. Finally queries **authoritative servers** for the actual record.

This allows the resolver to follow the DNS hierarchy until it finds the final IP address.

### 4. Recursive DNS Lookup (recursive_dns_lookup function)

#### TODO: Perform recursive resolution using the system's DNS resolver

This section uses the system's **recursive DNS resolver** (like Google DNS or an ISP resolver) to fetch DNS records.

#### Explanation:
1. First, the script queries for **NS records** to identify the responsible nameservers.
2. Then, it queries for the **A record** to resolve the domain to an IP address.

If any query fails, an error message is displayed.

## Challenges Faced
- **Insufficient response field size**: By default, UDP buffer has a 512 bytes size for response which is not sufficient for resolving all the nameserves. Resolved by enabling EDNS with a UDP buffer of 4096 bytes (refer to `send_dns_query()` function). By enabling this feature we are able to extract/resolve all the nameserver to ip_address from the additional field of response (i.e.,`response.additional`).


## Contribution Breakdown
| Member |Roll number| Contribution (%) | Tasks |
|--------|------|----------|-------|
| Denchanadula Rushikesh Chary      |  220336    |33.3%     | Code  |
| Pankaj Nath      |   221188   |33.3%     | Explanation/Comments |
| Saagar K V      |   220927   |33.3%     | README |

## References
- DNS python [manual](https://dnspython.readthedocs.io/en/latest/manual.html)

## Declaration
We declare that this implementation is our own work and does not involve plagiarism.


## Performance
The script prints the time taken for the DNS resolution in seconds.

