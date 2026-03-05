
# PyDNS-Enum: Authoritative Subdomain Enumerator

### 🔍 Overview

**PyDNS-Enum** is a custom-built Python tool designed for targeted DNS reconnaissance. Instead of relying on standard public DNS resolvers, this script intelligently locates a target domain's **Primary Name Server (SOA MNAME)** and directly queries it. By combining authoritative server querying with wordlist-based brute-forcing, it effectively discovers hidden or unlisted subdomains.

### ✨ Key Features

* **Automated SOA Extraction:** Automatically queries Google's public IPv6 DNS to extract the Start of Authority (SOA) MNAME record for any given domain.
* **Authoritative Direct Querying:** Resolves the IPv4 address of the target's primary name server and directs all brute-force traffic directly to it, bypassing standard caching mechanisms.
* **Dual-Wordlist Brute Forcing:** Randomly samples subdomains from custom text files (like `dnsmap.txt` and `wordlist_TLAs.txt`) to hunt for valid A-records.
* **Scapy-Powered:** Built entirely using Python's `scapy` library for granular, packet-level network control.

### 🚀 Usage

Run the script directly from your terminal, passing the target domain as the only argument:

```bash
python dns_enumerator.py example.com

```

### 🛠️ Prerequisites

This script requires Python 3 and the `scapy` library.

```bash
pip install scapy

```

*(Note: You will also need to have your wordlist files—`dnsmap.txt` and `wordlist_TLAs.txt`—in the same directory as the script).*

### ⚠️ Disclaimer

This tool was created for educational purposes and authorized penetration testing only. Do not use this script against networks or domains you do not own or have explicit permission to test.

