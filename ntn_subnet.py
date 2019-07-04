import ipaddress

def ntn_subnet(ip_address, subnet_mask):

    try:

        if '/' in subnet_mask:

            subnet = (ipaddress.ip_network(ip_address + subnet_mask, strict=False))

        else:

            subnet = (ipaddress.ip_network(ip_address + '/' + subnet_mask, strict=False))

    except ValueError:

        return {'Error': 'Invalid input'}

    return {
        'Network Address': subnet.network_address,        
        'Subnet Mask': subnet.netmask,
        'Wildcard Bits': subnet.hostmask,
        'Broadcast Address': subnet.broadcast_address,
        'Number of Address': subnet.num_addresses,
        'First Host': subnet.network_address + 1,
        'Last Host': subnet.broadcast_address - 1
    }