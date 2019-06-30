import dns.resolver

_RESOLVER_LIST = ['8.8.8.8', '4.2.2.2', '1.1.1.1', '9.9.9.9']

def ntn_dns(hostname, record_type):

    results = []

    for resolver in _RESOLVER_LIST:

        dns.resolver.override_system_resolver(resolver)

        try:
            response = dns.resolver.Resolver().query(hostname, record_type)
        except dns.resolver.NoAnswer:
            response = ['No Answer']
        except dns.resolver.NoNameservers:
            response = ['SERVFAIL']
        except dns.resolver.NXDOMAIN:
            response = ['NXDOMAIN']
            
        results.append({'response': response[:], 'resolver': resolver})

    dns.resolver.restore_system_resolver()

    return results

if __name__ == "__main__":

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

            print(result['response'])
            print(result['resolver'])