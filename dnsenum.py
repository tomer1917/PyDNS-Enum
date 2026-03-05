from scapy.all import *
import sys
import re


#generated method to extract subdomain names from txt file
def extract_sub_array(filepath):
    my_python_list = []

    with open(filepath, 'r') as file:
        content = file.read()

        # This regex looks for anything enclosed in double quotes
        # It will extract "apple", "banana", etc.
        matches = re.findall(r'"([^"]*)"', content)

        my_python_list.extend(matches)

    return my_python_list

#generated method to extract subdomain names from txt file
def get_names_from_txt(filepath):
    names_list = []

    # Open the text file in read mode ('r')
    with open(filepath, 'r') as file:
        for line in file:
            # .strip() removes spaces and the hidden '\n' (Enter key) from the line
            clean_word = line.strip()

            # Make sure we don't add empty blank lines to our list
            if clean_word:
                names_list.append(clean_word)

    return names_list

def getPrimaryServerName(domain_name):
    # SOA is type 6
    p = IPv6(dst='2001:4860:4860::8888') / UDP(dport=53) / DNS(rd=1, qdcount=1,
                                                               qd=DNSQR(qname=domain_name.encode(), qtype=6, qclass=1))
    r = sr1(p, 5)
    if (r != None):
        if (r.haslayer(DNS) and r[DNS].an is not None and hasattr(r[DNS].an, 'mname')):
            print("\n**** primary name server = " + r[DNS].an.mname.decode())
            return r[DNS].an.mname.decode()
        else:
            print("mname attribute not found in an section")
    else:
        print("domain not found")
        exit()



def getIpFromName(mname):
    p = IPv6(dst='2001:4860:4860::8888') / UDP(dport=53) / DNS(rd=1, qdcount=1,qd=DNSQR(qname=mname.encode(), qtype=1, qclass=1))
    r = sr1(p, timeout=0.2)
    ips = []
    if (r != None):
        #r.show()
        ancount = r[DNS].ancount
        for i in range(ancount):
            print("\n****server ip number "+ str(i + 1) +": "+ r[DNS].an[i].rdata)
            ips.append(r[DNS].an[i].rdata)
    else:
        print("ip timeout: could find ip")
        exit()

    return ips


def findSubDomains(dns_ip, domain_name, testAmount):
    #generate subdomain sample from txt files
    dnsmap = extract_sub_array("dnsmap.txt")
    wordlist = get_names_from_txt("wordlist_TLAs.txt")
    subdomainSamples = []
    startPoint1 = random.randint(1, len(wordlist))
    startPoint2 = random.randint(1, len(dnsmap))

    for i in range(testAmount):
        subdomainSamples.append(wordlist[(i+ startPoint1) % len(wordlist)])
    for i in range(testAmount):
        subdomainSamples.append(dnsmap[(i+ startPoint2) % len(dnsmap)])


    # subdomainSamples.append('moodle')


    #send dns packet to these domains
    result = []
    resultNames = []

    for i in range(len(subdomainSamples)):
        current_name = subdomainSamples[i] + "." +domain_name
        print("testing "+ current_name)
        p = IP(dst=dns_ip) / UDP(dport=53) / DNS(rd=1, qdcount=1,
                                                                   qd=DNSQR(qname=current_name.encode(), qtype=1, qclass=1))
        r = sr1(p, timeout=0.2)
        if (r != None):
            #r.show()
            ancount = r[DNS].ancount
            for i in range(ancount):
                print("!!!!!!!! found " + str(r[DNS].an[i].rdata ))
                resultNames.append(current_name)
                result.append(r[DNS].an[i].rdata)

    return result, resultNames





domain_name = ""
if len(sys.argv) > 1:
    domain_name = sys.argv[1]
    print("selected domain name: " + domain_name +"\n")
else:
    print("Error: Please provide a string parameter!")
    exit()


#find the domain primary name server
mname = getPrimaryServerName(domain_name=domain_name)

#find its ip
dns_ip = getIpFromName(mname)

#map the domain by sending dns packets to dns_ip
result , resultNames= findSubDomains(dns_ip = dns_ip,domain_name= domain_name, testAmount= 100)
print("\n************result: \n")
print(result)
print(resultNames)





