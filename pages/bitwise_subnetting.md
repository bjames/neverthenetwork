title: Bitwise Operations and Subnetting
published: 2019-07-29
category: 
 - Route/Switch
 - Programming
author: Brandon James
summary: I wrote a simple subnet calculator in C. Here are my takeaways from the process and some information on how it works. 

Back in September of 2016 I wrote a [subnet calculator in C](https://github.com/bjames/subnet) and then blogged about it. This entry is based on that old blog post.

### Converting To and From Dotted Decimal Notation

IPv4 Addresses are simply unsigned 32-bit integers. This makes it easy to perform calculations on them using bitwise operations. It's common to see IP addresses represented as four seperate octets. This is done primarily for readablity, but it also aids in intuition when you start looking at the math behind IP subnets. In order to get computers to play well with subnets, we first need to take the human readable dotted decimal notation and convert it back to a 32 bit unsigned integer. 

```c
unsigned int dotted_decimal_to_int(char ip[]){
 
    // char is exactly 1 byte
    unsigned char bytes[4] = {0};
    
    sscanf(ip, "%hhd.%hhd.%hhd.%hhd", &bytes[3], &bytes[2], &bytes[1], &bytes[0]);
    
    // set 1 byte at a time by left shifting and ORing
    return bytes[0] | bytes[1] << 8 | bytes[2] << 16 | bytes[3] << 24;

}
```

This function works by scanning the C string containing the IP address provided by the user into an array of bytes. It then returns an unsigned integer. Using 192.168.0.1 as an example, we first read the octets into an arry of bytes. This results in something similar to the following in memory:

<table>
  <tr>
    <th>Byte 0</th>
    <th>Byte 1</th>
    <th>Byte 2</th>
    <th>Byte 3</th>
    <th>Base</th>
  </tr>
  <tr>
    <td>192</td>
    <td>168</td>
    <td>0</td>
    <td>1</td>
    <td>Decimal</td>
  </tr>
  <tr>
    <td>11000000<br></td>
    <td>10101000</td>
    <td>00000000</td>
    <td>00000001</td>
    <td>Binary</td>
  </tr>
</table>