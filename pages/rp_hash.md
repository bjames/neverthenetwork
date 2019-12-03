title: Bootstrap Router Hash Function
category:
- Route/Switch
author: Brandon James
summary: 

[RFC 7761](https://tools.ietf.org/html/rfc7761#section-4.7.2) describes a hash function used to load balance multicast groups between RP candidates. This hash function isn't straight forward and I was unable to find a resource that described exactly how it worked. Since the hash mask length has a direct impact on how RP selection happens it's important to understand how this function works. I do my best to describe it here. 

## The Hash Function

The RFC describes the function as follows:

```
Value(G,M,C(i))=(1103515245 * ((1103515245 * (G&M)+12345) XOR C(i)) + 12345) mod 2^31
```

Where `C(i)` is the RP address, `M` is a hash-mask and `G` is the multicast group address. The RFC goes on to state that for non-IPv4 networks, a derivation function should be used to make `C(i)`, `M` and `G` 32-bit values. While not stated explicitly in the RFC, this seems to imply all values used in the function and the result of the function should be unsigned 32-bit integers. 

## Finding The Hash Value

Let's assume we have the following:

`C(i)`= 192.168.1.1

`M`= 30

`G`= 239.192.168.1

In binary, each of these values becomes:

Value | Byte 0 | Byte 1 | Byte 2 | Byte 3 |
---|---|---|---|---|
`C(i)` | `1100 0000` | `1010 1000` | `0000 0001` | `0000 0001` |
`M` | `1111 1111` | `1111 1111` | `1111 1111` | `1111 1100` |
`G` | `1110 1111` | `1100 0000` | `1010 1000` | `0000 0001` |

Now, let's manually work out the function. 

1. `(G&M)`

Value | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Operation
---|---|---|---|---|---|
 `G` | `1110 1111` | `1100 0000` | `1010 1000` | `0000 0001` |
 `M` | `1111 1111` | `1111 1111` | `1111 1111` | `1111 1100` | AND
 Result | `1110 1111` | `1100 0000` | `1010 1000` | `0000 0000`
 
 Note that `(G&M)` is __4022380544__ in Decimal
 
 2. `1103515245 * (G&M)+1234`
 
Value | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Operation
---|---|---|---|---|---|
1103515245 | `0100 0001` | `1100 0110` | `0100 1110` | `0110 1101` |
`(G&M)` | `1110 1111` | `1100 00001` | `1010 1000` | `0000 0000` | * |
Result | `1011 1000` | `0011 0111` | `1000 1000` | `0000 0000` |

Note that the result here is __3090647040__ in decimal. Let's call this `n` for the time being.

Value | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Operation |
---|---|---|---|---|---|
`n` | `1011 1000` | `0011 0111` | `1000 1000` | `0000 0000` |
12345 | `0000 0000` | `0000 0000` | `0011 0000` | `0011 1001` | + |
Result | `1011 1000` | `0011 0111` | `1011 1000` | `0011 1001` |

Note that the result here is __3090659385__. Let's call this `m`.

3. (1103515245 * ((1103515245 * (G&M)+12345) XOR C(i)) + 12345


Value | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Operation
---|---|---|---|---|---|
1103515245 | `0100 0001` | `1100 0110` | `0100 1110` | `0110 1101` |
`m` | `1011 1000` | `0011 0111` | `1011 1000` | `0011 1001` | * 
Result | `0101 1110` | `1111 0000` | `1100 1110` | `0100 0101` |

Note that the result here is __1592839749__ in Decimal. Let's call this `o`.

Value | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Operation
---|---|---|---|---|---|
`o` | `0101 1110` | `1111 0000` | `1100 1110` | `0100 0101` |
`C(i)` | `1100 0000` | `1010 1000` | `0000 0001` | `0000 0001` | XOR
Result | `1001 1110` | `0101 1000` | `1100 1111` | `0100 0100` | 
 
Note that the result here is __2656620356__ in Decimal. Let's call this `p`. 

Value | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Operation
---|---|---|---|---|---|
`p` | `1001 1110` | `0101 1000` | `1100 1111` | `0100 0100` |
1234 | `0000 0000` | `0000 0000` | `0000 0100` | `1101 0010` | + |
Result | `1001 1110` | `0101 1000` | `1111 1111` | `0111  1101` | 

Note that the result here is __2656632701__ in Decimal. Let's call this `q`

4. Value(G,M,C(i))=(1103515245 * ((1103515245 * (G&M)+12345) XOR C(i)) + 12345) mod 2^31

Value | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Operation
---|---|---|---|---|---|
`q` | `1001 1110` | `0101 1000` | `1111 1111` | `0111  1101` | 
2<sup>31</sup> | `1000 000` | `0000 0000` | `0000 0000` | `0000 0000` | %
Result | `0001 1110` | `0101 1000` | `1111 1111` | `0111 1101`|

Note that result here is __509149053__. This is our hash value. 

## Using Numpy and ipaddress to Calculate Hash Values

```
import ipaddress

from numpy import uint32, bitwise_and, bitwise_xor

def calculate_hash(rp_address, group, mask):

    result = uint32(bitwise_and(group,mask))
    result = uint32(uint32(1103515245) * uint32(result)) + uint32(12345)
    result = uint32(uint32(1103515245) * uint32(result))
    result = uint32(bitwise_xor(result, rp_address))
    result = uint32(uint32(result) + uint32(12345))
    result = uint32(uint32(result) % uint32(2**31))

    return result

if __name__ == '__main__':

    prompt = False

    while prompt:
        rp_address = uint32(ipaddress.IPv4Address(input('Enter RP Candidate Address: ')))
        group = uint32(ipaddress.IPv4Address(input('Enter multicast Group Address: ')))
        mask_length = uint32(int(input('Enter mask length: ')))
        mask = uint32((2**mask_length) - 1 << 32-mask_length)

        print(calculate_hash(rp_address, group, mask))

    rp_address = uint32(ipaddress.IPv4Address('192.168.1.1'))
    group = uint32(ipaddress.IPv4Address('239.192.168.1'))
    mask_length = uint32(30)
    mask = uint32((2**mask_length) - 1 << 32-mask_length)

    print(calculate_hash(rp_address, group, mask))
```