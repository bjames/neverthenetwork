DNS_ROOT_SERVERS = [
    'a.root-servers.net', 'b.root-servers.net', 'c.root-servers.net',
    'd.root-servers.net', 'e.root-servers.net', 'f.root-servers.net',
    'g.root-servers.net', 'h.root-servers.net', 'i.root-servers.net',
    'j.root-servers.net', 'k.root-servers.net', 'l.root-servers.net',
    'm.root-servers.net'
]

DNS_RESOLVER_LIST = [
    {'name': 'Google', 'ip': '8.8.8.8'},
    {'name': 'Level3', 'ip': '4.2.2.2'},
    {'name': 'CloudFlare', 'ip': '1.1.1.1'},
    {'name': 'Quad9', 'ip': '9.9.9.9'},
    {'name': 'OpenDNS', 'ip': '208.67.222.222'},
    {'name': 'Verisign', 'ip': '64.6.64.6'},
    {'name': 'AdGuard', 'ip': '176.103.130.131'},
    {'name': 'CleanBrowsing - Family Filter', 'ip': '185.228.168.168'}
]

DNS_RECORD_TYPES = [
    'A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT'
]

OUI_FILES = [
    {'url': 'http://standards-oui.ieee.org/oui/oui.csv', 'oui_length': 6, 'table_name': 'OUI_MAL'},
    {'url': 'http://standards-oui.ieee.org/oui28/mam.csv', 'oui_length': 7, 'table_name': 'OUI_MAM'},
    {'url': 'http://standards-oui.ieee.org/oui36/oui36.csv', 'oui_length': 9, 'table_name': 'OUI_MAS'}
]

DATABASE = 'sqlite:///ntn.db'

DATABASE_KEY = 'Th!s !s n0t cUst0mer Data'