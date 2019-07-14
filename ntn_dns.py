import dns.resolver
from config import DNS_RESOLVER_LIST, DNS_ROOT_SERVERS

def ntn_ns(hostname):

    pass

def ntn_dns(hostname, user_resolver, record_type):

    results = []
    resolvers = []

    dns_resolver = dns.resolver.Resolver()

    # if the user selects all resolvers, query all default resolvers (Does not include root servers)
    if user_resolver == 'All':

        resolvers = DNS_RESOLVER_LIST

    elif user_resolver == 'Root Servers':

        resolvers = DNS_ROOT_SERVERS

    else:

        # if the user selects a single resolver, we set that here
        for resolver in DNS_RESOLVER_LIST:

            if resolver['name'] == user_resolver:
                
                resolvers.append(resolver)

    for resolver in resolvers:

        dns_resolver.nameservers.clear()
        dns_resolver.nameservers.append(resolver['ip'])

        try:
            response = dns_resolver.query(hostname, record_type)
        except dns.resolver.NoAnswer:
            response = ['No Answer']
        except dns.resolver.NoNameservers:
            response = ['SERVFAIL']
        except dns.resolver.NXDOMAIN:
            response = ['NXDOMAIN']
        except dns.resolver.Timeout:
            response = ['Response timed out']

        result = [str(answer).strip('"') for answer in response]

        results.append({'response': sorted(result[:]), 'resolver': resolver})


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

        results = ntn_dns(request['hostname'], 'Root Servers', request['record_type'])

        for result in results:

            pprint(result)