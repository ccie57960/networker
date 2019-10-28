# networker

A library I'm creating with methods/functions useful to networking.

### Description of each method:

#### ipv4_to_binary(ip)
```Python
Convert "IP" to Binary (32 bits representation) --> list of str
  ip = 10.1.2.3 --> ["00001010", "00000001", "00000010", "00000011"]
  ip = 128.255.0.1 --> ["10000000", "11111111", "00000000", "00000001"]
```
#### ipv6_to_binary(ipv6="a")
```Python
Convert "IPv6" to Binary (128 bits representation) --> list of str
  ipv6 = 2001:db8::1 --> ['0010000000000001', '0000110110111000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000001']
  ipv6 = :: --> ['0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000']
```
#### ipv4mask_to_decimal(mask)
```Python
Convert "mask" to Decimal --> int
  mask = 255.255.255.0 --> 24
  mask = 255.255.255.255 --> 32
  mask = 128.0.0.0 --> 1
```
#### ipv4mask_from_decimal(bits)
```Python
Create "mask" in IPv4 format from Decimal (network bits) --> str
  bits = 24 --> 255.255.255.0
  bits = 32 --> 255.255.255.255
  bits = 1 --> 128.0.0.0
```
#### issubnetv4(ip, network, mask="")
```Python
Validate if "IP" belongs to the "network" (IP/MASK) --> boolean
  If "mask" (int or str) is specified network should be an IP

  ip = 10.1.2.3 network = 10.1.2.0/24 -->True
  ip = 10.1.2.3 network = 10.1.2.0 mask = 24 -->True
  ip = 10.1.2.3 network = 10.1.1.0/24 -->False
  ip = 10.1.2.3 network = 10.1.1.0 mask = 24 -->False
```
#### ios_ospf_lsa2(lsa2)
```Python
Based on "show ip ospf 1 0 database network" (Cisco IOS)
  recommended filter: "| include Routing|Designated|Mask|Attached"
  return dictionary as follow:
  {dr_ip:{"network":dr_ip/mask, "routers":(r1, r2,...,rn)}}
  {10.7.8.7:{"network":10.7.8.7/24, "routers":(10.7.8.7, 10.7.8.1,...,10.7.8.2)}}

  Example for OSPF process-ID:1 and area:0
  **Single Area support "at once"
```
#### ios_ospf_lsa1(lsa1, dict_lsa2 = {})
```Python
Based on "show ip ospf 1 0 database router" (Cisco IOS)
  recommended filter: "| include Link State ID|Link connected to|(Link ID)|Metrics"
  In case your network has LSA Type 2, firstly run "ios_ospf_lsa2"
  and provide the output dictionary to this method, if not, LSA type 2 will be ignored.

  return dictionary as follow:
  {
   "node1":
     {"node1_neighbor1": [list of metric], "node1_neighbor2":[list of metric]},
   "node2":
     {"node2_neighbor1": [list of metric], "node1_neighbor2":[list of metric]},
  }

  {
   '10.0.0.7':
     {'10.0.0.77': [10], '10.0.0.8': [10], '10.0.0.9': [10]},
   '10.0.0.8':
     {'10.0.0.10': [10], '10.0.0.12': [10], '10.0.0.9': [10, 10], '10.0.0.77': [10], '10.0.0.7': [10]}
  }

  Example for OSPF process-ID:1 and area:0
  **Single Area support "at once"
```
#### sh_lsa1()
```Python
For testing/illustration purpose - From Cisco IOS
show ip ospf 1 0 database router.
In real life you may use an SSH client (ie: Napalm or Netmiko)
to get the show output or any other method you may prefer.
```
#### sh_lsa2()
```Python
For testing purpose - From Cisco IOS
show ip ospf 1 0 database network.
In real life you may use an SSH client (ie: Napalm or Netmiko)
to get the show output or any other method you may prefer.
```
Feel free to use, modify, share it. Any feedback would be appreciated :D Also you could optionally donate (https://www.paypal.me/57960)


Hope this may help you.
