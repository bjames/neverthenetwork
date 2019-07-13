import ipaddress

def ntn_subnet(ip_address, subnet_mask):

    try:

        if '/' in subnet_mask:

            subnet = (ipaddress.ip_network(ip_address + subnet_mask, strict=False))

        else:

            subnet = (ipaddress.ip_network(ip_address + '/' + subnet_mask, strict=False))


    except ValueError:

        return {'Error': 'Invalid subnet mask or IP address'}

    address_type = ''

    try:

        if subnet.is_global:

            address_type += 'Public '

    except AttributeError:

            pass

    try:

        if subnet.is_private:

            address_type += 'Private '
        
    except AttributeError:

            pass

    try:

        if subnet.is_multicast:

            address_type += 'Multicast '
        
    except AttributeError:

        pass

    try:

        if subnet.is_link_local:

            address_type += 'Link Local '

    except AttributeError:

        pass

    try:
        
        if subnet.is_site_local:

            address_type += 'Site Local '

    except AttributeError:

        pass

    try:

        if subnet.is_loopback:

            address_type += 'Loopback '

    except AttributeError:

        pass

    try:

        if subnet.is_reserved:

            address_type += 'Reserved '

    except AttributeError:

        pass

    if address_type == '':

        address_type = "Undefined (Range may span private, public and/or multicast address space)"


    if subnet.num_addresses == 1:

        return {
            'Network Address': subnet.network_address,        
            'Subnet Mask': subnet.netmask,
            'CIDR': '/{}'.format(subnet.prefixlen),
            'Wildcard Bits': subnet.hostmask,
            'Number of Addresses': subnet.num_addresses,
            'Address Type': address_type
        }
        
    elif subnet.num_addresses == 2:

        return {
            'Subnet Mask': subnet.netmask,
            'CIDR': '/{}'.format(subnet.prefixlen),
            'Wildcard Bits': subnet.hostmask,
            'Number of Addresses': subnet.num_addresses,
            'First Host': subnet.network_address,
            'Last Host': subnet.broadcast_address,
            'Address Type': address_type
        }

    else:

        return {
            'Network Address': subnet.network_address,        
            'Subnet Mask': subnet.netmask,
            'CIDR': '/{}'.format(subnet.prefixlen),
            'Wildcard Bits': subnet.hostmask,
            'Broadcast Address': subnet.broadcast_address,
            'Number of Addresses': subnet.num_addresses,
            'First Host': subnet.network_address + 1,
            'Last Host': subnet.broadcast_address - 1,
            'Address Type': address_type
        }