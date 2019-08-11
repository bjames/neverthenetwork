If you're a Network Engineer, you've probably heard of LISP. You may be aware that SDN solutions such as Cisco DNA use it, you may have heard that it allows subnets to be used in multiple locations (without NAT) and you might even know that it's existence is owed largely to routing table growth in the default-free zone. However, if you aren't in the provider space, you've probably never touched it and unless you've bothered to learn about it in your free time, it's unlikely that you fully understand why it exists or what it does. 

# Why it exists

The Location/Identifier Separation Protocol was formally ratified under [RFC 6830](https://tools.ietf.org/html/rfc6830). I think the following quote from the RFC is the best summary of the problem LISP attempts to solve:

>for routing to be efficient, the [ip] address must be assigned topologically; for collections of devices to be easily and effectively managed, without the need for renumbering in response to topological change (such as that caused by adding or removing attachment points to the network or by mobility events), the address must explicitly not be tied to the topology.

In a perfect world (at least from the perspective of a DFZ router), all IP speaking devices would be distributed uniformly throughout the globe, ISPs would never suffer outages so enterprises wouldn't need to multi-home their internet connections and [RFC 790](https://tools.ietf.org/html/rfc790) would've never existed (37.0.0.0/8 might belong to Texas or Ontario instead of DEC). This would make it trivial for carriers to aggregate routes based on region. 

As any one who's tried to roll their own GeoIP database can tell you, this simply isn't how things work. Overtime, ISPs have been forced to disaggregate due to both multi-homing and the increased need for IP space. Which is why we've ended up with over [700,000 routes (and counting)](https://www.cidr-report.org/as2.0/) in the DFZ. While LISP doesn't do much to solve IPv4 exhaustion, it can help decrease the number of routes in the DFZ. 

# Basic Terms

* *Routing Locators (RLOCs)* - RLOCs are 32 or 128-bit integers used to describe a location

* *Endpoint Identifiers (EIDs)* - EIDs are 32 or 128-bit integers used to describe an endpoint

_Note both RLOCs and EIDs are written using the traditional dotted decimal format we use for IPs_

* *Tunnel Router* - Adds LISP headers to host originated packets and strips them prior to final delivery


# How it works

LISP works by replacing IP addresses with two separate numbers, Routing Locators (RLOCs) and Endpoint Identifiers (EIDs). RLOCs are assigned based on region, whereas EIDs are assigned to specific endpoints. RLOCs are routable (using LISP), EIDs are not. RLOCs and EIDs are both 32 bit integers represented exactly like IP addresses (Note: These may also be represented as 128-bit integers, exactly like IPv6). 

### The EID-to-RLOC database

Understanding that LISP uses a database mapping EIDs to RLOCs is probably enough for most network engineers. In order to aid with translation from standard IPv4 routing to LISP, EIDs (and EID-prefixs) can be routable IPv4 addresses (See [RFC 6832](https://tools.ietf.org/html/rfc6832) for how this transition is meant to look). In fact, from the perspective of endpoints nothing changes with LISP, it's still just speaking IP. 
 

