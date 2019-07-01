import dns.resolver

_ROOT_SERVERS = [
    'a.root-servers.net', 'b.root-servers.net', 'c.root-servers.net',
    'd.root-servers.net', 'e.root-servers.net', 'f.root-servers.net',
    'g.root-servers.net', 'h.root-servers.net', 'i.root-servers.net',
    'j.root-servers.net', 'k.root-servers.net', 'l.root-servers.net',
    'm.root-servers.net'
]

_RESOLVER_LIST = [
    {'name': 'Google', 'ip': '8.8.8.8'},
    {'name': 'Level3', 'ip': '4.2.2.2'},
    {'name': 'CloudFlare', 'ip': '1.1.1.1'},
    {'name': 'Quad9', 'ip': '9.9.9.9'},
    {'name': 'OpenDNS', 'ip': '208.67.222.222'},
    {'name': 'Verisign', 'ip': '64.6.64.6'},
    {'name': 'AdGuard', 'ip': '176.103.130.131'},
    {'name': 'CleanBrowsing (Family Filter)', 'ip': '185.228.168.168'}
]

RECORD_TYPES = [
    'A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT'
]

def ntn_ns(hostname):

    pass

def ntn_dns(hostname, record_type):

    results = []

    dns_resolver = dns.resolver.Resolver()

    for resolver in _RESOLVER_LIST:

        dns_resolver.nameservers.clear()
        dns_resolver.nameservers.append(resolver['ip'])
        print(dns_resolver.nameservers)

        try:
            response = dns_resolver.query(hostname, record_type)
        except dns.resolver.NoAnswer:
            response = ['No Answer']
        except dns.resolver.NoNameservers:
            response = ['SERVFAIL']
        except dns.resolver.NXDOMAIN:
            response = ['NXDOMAIN']
        
        results.append({'response': response[:], 'resolver': resolver})


    try:
        return results.rrset
    except:
        return results

if __name__ == "__main__":

    from pprint import pprint

    test_request = [
        {'hostname': 'brandonsjames.com', 'record_type': 'A'},
        {'hostname': 'brandonsjames.com', 'record_type': 'AAAA'},
        {'hostname': 'brandonsjames.com', 'record_type': 'CNAME'},
        {'hostname': 'brandonsjames.com', 'record_type': 'DNAME'},
        {'hostname': 'brandonsjames.com', 'record_type': 'MX'},
        {'hostname': 'brandonsjames.com', 'record_type': 'NS'},
        {'hostname': 'brandonsjames.com', 'record_type': 'PTR'},
        {'hostname': 'brandonsjames.com', 'record_type': 'SOA'},
        {'hostname': 'brandonsjames.com', 'record_type': 'SRV'},
        {'hostname': 'brandonsjames.com', 'record_type': 'TXT'},
    ]

    for request in test_request:

        results = ntn_dns(request['hostname'], request['record_type'])

        for result in results:

            pprint(result)