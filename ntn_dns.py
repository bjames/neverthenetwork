import dns.resolver

_RESOLVER_LIST = ['8.8.8.8', '4.2.2.2', '1.1.1.1']

def ntn_dns(hostname):

    results = []

    for resolver in _RESOLVER_LIST:

        dns.resolver.override_system_resolver(resolver)

        response = dns.resolver.Resolver().query(hostname, 'A')

        results.append({'response': response[:], 'resolver': resolver})

    dns.resolver.restore_system_resolver()

    return results