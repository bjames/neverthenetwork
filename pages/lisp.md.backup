title: Locator/ID Separation Protocol - LISP
category:
- Route/Switch
author: Brandon James
summary: 

The Locator/ID Separation Protocol or LISP was originally designed to decrease the size of routing tables in Internet routers. As the protocol matured it made it's way into the enterprise[^1] though solutions like Cisco SDA[^2]. In this article I provide a summary of why LISP exists and how it functions. The purpose of this article isn't to provide a validated design, but to build an awareness around LISP.

# Why LISP Exists

LISP was formally ratified under [RFC 6830](https://tools.ietf.org/html/rfc6830). The quote from the RFC is the best summary for the problem LISP solves:

>for routing to be efficient, the address must be assigned topologically; for collections of devices to be easily and effectively managed, without the need for renumbering in response to topological change (such as that caused by adding or removing attachment points to the network or by mobility events), the address must explicitly not be tied to the topology.

In a perfect world (at least from the perspective of an Internet router), all IP speaking devices would be distributed uniformly throughout the globe, ISPs would never suffer outages so enterprises wouldn't need to multi-home their internet connections and [RFC 790](https://tools.ietf.org/html/rfc790) would've never existed (37.0.0.0/8 might belong to Texas or Ontario instead of DEC). This would make it trivial for carriers to aggregate routes based on region. 

Unfortunately, this simply isn't how things work. Overtime, ISPs have been forced to disaggregate due to both multi-homing and the increased demand for IP space. Which is why we've ended up with over [700,000 routes (and counting)](https://www.cidr-report.org/as2.0/) in Internet routing tables. While LISP doesn't do much to solve IPv4 exhaustion, it can help decrease the size of Internet routing tables. 

# Basic Terms


* __Routing Locators (RLOCs)__ - RLOCs are 32 or 128-bit integers used to describe a location

* __Endpoint Identifiers (EIDs)__ - EIDs are 32 or 128-bit integers used to identify an endpoint

_Note: both RLOCs and EIDs are written using the traditional dotted decimal format we use for IPs_

* __Tunnel Routers (xTR)__ - Encapsulates IP packets leaving LISP sites and decapsulates IP packets entering LISP sites.
	- __Ingress Tunnel Router (ITR)__ - Tunnel Router that performs encapsulation and looks up EID-to-RLOC mappings
	- __Egress Tunnel Router (ETR)__ - Tunnel Router that performs decapsulation and acts as an authoritative source for EID-to-RLOC mappings
* __Map Server__ - Learns authoritative EID-to-RLOC mappings from ETRs and publishes them in a mapping database
* __Map Resolver__ - Resolves Map-Requests from ITRs using a mapping database

# How it works

! Provide a better summary here

LISP works by replacing IP addresses with Routing Locators and Endpoint Identifiers. RLOCs are assigned based on region, whereas EIDs are assigned to specific endpoints. RLOCs are routable throughout an AS, EIDs are not. RLOCs and EIDs are both 32 or 128-bit integers represented exactly like IP addresses. 

## Communication between endpoints

LISP endpoints continue to speak IP exactly like they do today. From the perspective of a LISP router, each endpoint has an EID, but from the perspective of the endpoint itself, it has an IP address. In addition, endpoints only send traffic to EIDs. The general flow for a packet sent from an endpoint is (1) the endpoint sends a packet destined to an EID, (2) the LISP router receives the packet and looks up the destination EID in the EID-to-RLOC database, (3) the router encapsulates the packet and forwards it to the destination RLOC and (4) the destination router decapsulates the packet and forwards it to the destination endpoint.

## LISP Packet Format

LISP operates as similarly to a tunnel using IP-in-IP encapsulation. I've copied the example packet format from [RFC 6830](https://tools.ietf.org/html/rfc6830) section 5.1 below.

```
        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |Version|  IHL  |Type of Service|          Total Length         |
    /  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |         Identification        |Flags|      Fragment Offset    |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   OH  |  Time to Live | Protocol = 17 |         Header Checksum       |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |                    Source Routing Locator                     |
    \  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                 Destination Routing Locator                   |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |       Source Port = xxxx      |       Dest Port = 4341        |
   UDP +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |           UDP Length          |        UDP Checksum           |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   L   |N|L|E|V|I|flags|            Nonce/Map-Version                  |
   I \ +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   S / |                 Instance ID/Locator-Status-Bits               |
   P   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     / |Version|  IHL  |Type of Service|          Total Length         |
    /  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |         Identification        |Flags|      Fragment Offset    |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   IH  |  Time to Live |    Protocol   |         Header Checksum       |
   |   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |   |                           Source EID                          |
    \  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     \ |                         Destination EID                       |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

       IHL = IP-Header-Length
       
```

I'm not going to go into detail on the packet format here, just note that the LISP header is sandwiched between the inner and outer IP headers.

## EID-to-RLOC Resolution

The EID-to-RLOC Mapping service operates similarly to DNS, but instead of domain-to-IP mappings, it provides EID-to-RLOC mappings. The method used to provide mappings in the LISP beta network is called LISP Alternative Logical Topology or LISP+ALT. [RFC 6836](https://tools.ietf.org/html/rfc6836) describes LISP+ALT in detail. There are other standards for LISP databases and all provide a common interface for LISP routers. I'm not going to spend much time discussing the database implementation and instead we will focus on the standard interface they provide.

In addition to the definitions found in [RFC 6830](https://tools.ietf.org/html/rfc6830), [RFC 6833](https://tools.ietf.org/html/rfc6833) defines the Map-Server interface and expands on the message types the interface uses. The message types are summarized below:

### LISP Map-Request

Map-Request messages are primarily used to request EID-to-RLOC mappings in the case of a cache-miss. Map-Requests originate from an ITR and are sent to Map-Resolvers. The Map-Resolvers will then respond with a Map-Reply if the mapping is in it's local database,   

### LISP Map-Reply

! Are they only sent from ETRs?

Map-Reply messages are sent from ETRs and are primarily used to provide EID-to-RLOC mappings in response to Map-Requests.

### LISP Map-Register

### LISP Map-Notify

### LISP Encapsulated Control Message

[^1]: The creators of LISP noted it's potential use in the enterprise. See Dino Farinacci's talk [here](http://www.youtube.com/watch?v=fxdm-Xouu-k)

[^2]: This [whitepaper](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise-networks/software-defined-access/white-paper-c11-740585.pdf) provides a brief summary on how LISP is used in SDA. Note that LISP is only used for control plane traffic.