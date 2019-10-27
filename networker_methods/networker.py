#!/usr/bin/env python
'''Some useful networking methods
'''

def ipv4_to_binary(ip):
    '''Convert "IP" to Binary (32 bits representation) --> list of str
    ip = 10.1.2.3 --> ["00001010", "00000001", "00000010", "00000011"]
    ip = 128.255.0.1 --> ["10000000", "11111111", "00000000", "00000001"]
    '''
    list_oct = ip.split(".")
    list_binary = [format(int(octect), "08b") for octect in list_oct]
    return list_binary

def ipv6_to_binary(ipv6="a"):
    '''Convert "IPv6" to Binary (128 bits representation) --> list of str
    ipv6 = 2001:db8::1 --> ['0010000000000001', '0000110110111000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000001']
    ipv6 = :: --> ['0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000']
    '''
    ipv6 = ipv6.split(":")

    if len(ipv6) < 8:
        break_point = ipv6.index("")
        ipv6[break_point] = "0000"

        while len(ipv6) < 8:
            ipv6.insert(break_point, "0000")

    for index, nibble in enumerate(ipv6):
        if len(nibble) < 4:
            #Represent each nibble as 4 char/hex - add leading zeros
            ipv6[index] = format(ipv6[index], "0>4s")

    list_binary = [format(int(nibble, 16), "016b") for nibble in ipv6]
    return list_binary

def ipv4mask_to_decimal(mask):
    '''Convert "mask" to Decimal --> int
    mask = 255.255.255.0 --> 24
    mask = 255.255.255.255 --> 32
    mask = 128.0.0.0 --> 1
    '''
    network_bits = 0
    mask = "".joint(ip2binary(mask))
    network_bits = mask.count("1")

    return network_bits

def ipv4mask_from_decimal(bits):
    '''Create "mask" in IPv4 format from Decimal (network bits) --> str
    bits = 24 --> 255.255.255.0
    bits = 32 --> 255.255.255.255
    bits = 1 --> 128.0.0.0
    '''
    bits = int(bits)
    mask = "1"*bits + "0"*(32-bits)

    return str(int(mask[:8],2)) + "." + str(int(mask[8:16],2)) + "." + str(int(mask[16:24],2)) + "." + str(int(mask[24:],2))

def issubnetv4(ip, network, mask=""):
    '''Validate if "IP" belongs to the "network" (IP/MASK) --> boolean
    If "mask" (int or str) is specified network should be an IP

    ip = 10.1.2.3 network = 10.1.2.0/24 -->True
    ip = 10.1.2.3 network = 10.1.2.0 mask = 24 -->True
    ip = 10.1.2.3 network = 10.1.1.0/24 -->False
    ip = 10.1.2.3 network = 10.1.1.0 mask = 24 -->False
    '''

    if mask == "":
        network,mask = network.split("/")

    mask = int(mask)
    ip = "".join(ipv4_to_binary(ip))
    network = "".join(ipv4_to_binary(network))
    network = network[:mask]
    ip = ip[:mask]

    return ip == network

def ios_ospf_lsa2(lsa2):
    '''Based on "show ip ospf 1 0 database network" (cisco IOS)
    recommended filter: "| include Routing|Designated|Mask|Attached"
    return dictionary as follow:
    {dr_ip:{"network":dr_ip/mask, "routers":(r1, r2,...,rn)}}
    {10.7.8.7:{"network":10.7.8.7/24, "routers":(10.7.8.7, 10.7.8.1,...,10.7.8.2)}}

    Example for OSPF process-ID:1 and area:0
    **Single Area support "at once"
    '''
    lsa2 = lsa2.split("\n")
    valid = False
    dr = ""
    network = ""
    routers = []
    dict_lsa2 = {}
    for index, line in enumerate(lsa2):
        if valid:
            if "Link State ID" in line:
                dr = line.split()[3]
            elif "Network Mask" in line:
                network = dr
                network += line.split()[2]
            elif "Attached Router" in line:
                routers.append(line.split()[2])
                if "Attached Router" not in lsa2[index+1]:
                    dict_lsa2.update({dr:{"network":network, "routers":tuple(routers)}})
                    valid = False
                    dr = ""
                    network = ""
                    routers = []
        elif "Routing Bit Set" in line:
            valid = True

    return dict_lsa2

def ios_ospf_lsa1(lsa1, dict_lsa2 = {}):
    '''Based on "show ip ospf 1 0 database network" (cisco IOS)
    recommended filter: "| include Routing|Designated|Mask|Attached"
    return dictionary as follow:
    {dr_ip:{"network":dr_ip/mask, "routers":(r1, r2,...,rn)}}
    {10.7.8.7:{"network":10.7.8.7/24, "routers":(10.7.8.7, 10.7.8.1,...,10.7.8.2)}}

    Example for OSPF process-ID:1 and area:0
    **Single Area support "at once"
    '''

    lsa1 = lsa1.split("\n")
    routerid = ""
    adj_reference = ""
    metric_high = 65535*1.2 #higher than OSPF max interface cost
    metric = metric_high
    dict_lsa1 = {}
    network_type = ""
    warning_lsa2 = True

    for index, line in enumerate(lsa1):
        if "Link State ID" in line:
            routerid = line.split()[3]
            # network_type = ""
            # adj_reference = ""
            # metric = metric_high

        elif "Link connected to" in line:
            if "Stub Network" in line:
                continue
            elif "point-to-point" in line:
                network_type = "p2p"
            elif "Transit" in line:
                if dict_lsa2 == {}:
                    if warning_lsa2:
                        print("warning: Transit network found, but LSA2 not provided")
                        warning_lsa2 = False
                    continue
                network_type = "transit"
            else:
                raise Exception(f"Unsupported network type in:{line}")#Better a Warning

        elif network_type != "":
            if "(Link ID)" in line and "Router" in line:
                adj_reference = line.split()[-1]

            elif "Metrics" in line:
                metric = int(line.split()[-1])

                if network_type == "p2p":
                    if dict_lsa1.get(routerid):
                        if dict_lsa1[routerid].get(adj_reference):
                            dict_lsa1[routerid][adj_reference].append(metric)
                        else:
                            # dict_lsa1.update({routerid:{adj_reference:[metric]}})
                            dict_lsa1[routerid].update({adj_reference:[metric]})
                    else:
                        dict_lsa1.update({routerid:{adj_reference:[metric]}})

                elif network_type == "transit":
                    if not dict_lsa1.get(routerid):
                        dict_lsa1.update({routerid:{}})

                    for neighbor in dict_lsa2[adj_reference]['routers']:
                        if neighbor == routerid:
                            continue
                        else:
                            if dict_lsa1[routerid].get(neighbor):
                                dict_lsa1[routerid][neighbor].append(metric)
                            else:
                                # dict_lsa1.update({routerid:{neighbor:[metric]}})
                                dict_lsa1[routerid].update({neighbor:[metric]})
                network_type = ""
                adj_reference = ""
                metric = metric_high


    return dict_lsa1

def sh_lsa1():
    '''For testing porpose - From Cisco IOS
show ip ospf 1 0 database router
    '''
    return '''


R7#ter len 0
R7#show ip ospf 1 0 database router

            OSPF Router with ID (10.0.0.7) (Process ID 1)

                Router Link States (Area 0)

  LS age: 1173
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.7
  Advertising Router: 10.0.0.7
  LS Seq Number: 80000003
  Checksum: 0xCE8E
  Length: 72
  AS Boundary Router
  Number of Links: 4

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.7
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.2.7.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.3.7.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.7.89.77
     (Link Data) Router Interface address: 10.7.89.7
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


  LS age: 1180
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.8
  Advertising Router: 10.0.0.8
  LS Seq Number: 80000005
  Checksum: 0xB06D
  Length: 120
  Number of Links: 8

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.8
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.10
     (Link Data) Router Interface address: 10.8.10.8
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.8.10.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.12
     (Link Data) Router Interface address: 10.8.12.8
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.8.12.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.9
     (Link Data) Router Interface address: 10.8.9.8
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.8.9.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.7.89.77
     (Link Data) Router Interface address: 10.7.89.8
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


  LS age: 1175
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.9
  Advertising Router: 10.0.0.9
  LS Seq Number: 80000005
  Checksum: 0xC6DC
  Length: 96
  Number of Links: 6

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.9
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.10
     (Link Data) Router Interface address: 10.9.10.9
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.9.10.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.8
     (Link Data) Router Interface address: 10.8.9.9
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.8.9.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.7.89.77
     (Link Data) Router Interface address: 10.7.89.9
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


  LS age: 1180
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.10
  Advertising Router: 10.0.0.10
  LS Seq Number: 80000005
  Checksum: 0xC69
  Length: 96
  Number of Links: 6

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.10
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.8
     (Link Data) Router Interface address: 10.8.10.10
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.8.10.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.9
     (Link Data) Router Interface address: 10.9.10.10
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.9.10.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.10.11.11
     (Link Data) Router Interface address: 10.10.11.10
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


  LS age: 1175
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.11
  Advertising Router: 10.0.0.11
  LS Seq Number: 80000003
  Checksum: 0x13D6
  Length: 60
  Number of Links: 3

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.11
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.11.110.110
     (Link Data) Router Interface address: 10.11.110.11
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.10.11.11
     (Link Data) Router Interface address: 10.10.11.11
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


  LS age: 1205
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.12
  Advertising Router: 10.0.0.12
  LS Seq Number: 80000004
  Checksum: 0x2B79
  Length: 108
  Number of Links: 7

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.12
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.8
     (Link Data) Router Interface address: 10.8.12.12
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.8.12.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.120
     (Link Data) Router Interface address: 10.12.120.12
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.12.120.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.120
     (Link Data) Router Interface address: 10.120.12.12
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.120.12.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


  LS age: 1179
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.77
  Advertising Router: 10.0.0.77
  LS Seq Number: 80000003
  Checksum: 0x7928
  Length: 48
  Number of Links: 2

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.77
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.7.89.77
     (Link Data) Router Interface address: 10.7.89.77
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


  LS age: 173
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.110
  Advertising Router: 10.0.0.110
  LS Seq Number: 80000005
  Checksum: 0x5F63
  Length: 72
  Number of Links: 4

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.110
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.120
     (Link Data) Router Interface address: 10.110.120.110
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.110.120.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.11.110.110
     (Link Data) Router Interface address: 10.11.110.110
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


  LS age: 172
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.120
  Advertising Router: 10.0.0.120
  LS Seq Number: 80000006
  Checksum: 0xC61E
  Length: 108
  Number of Links: 7

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.120
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.110
     (Link Data) Router Interface address: 10.110.120.120
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.110.120.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.12
     (Link Data) Router Interface address: 10.12.120.120
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.12.120.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.12
     (Link Data) Router Interface address: 10.120.12.120
      Number of MTID metrics: 0
       TOS 0 Metrics: 10

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.120.12.0
     (Link Data) Network Mask: 255.255.255.0
      Number of MTID metrics: 0
       TOS 0 Metrics: 10


R7#

'''

def sh_lsa2():
    '''For testing porpose - From Cisco IOS
show ip ospf 1 0 database network
    '''
    return '''

R7#show ip ospf 1 0 database net
R7#show ip ospf 1 0 database network

            OSPF Router with ID (10.0.0.7) (Process ID 1)

                Net Link States (Area 0)

  Routing Bit Set on this LSA in topology Base with MTID 0
  LS age: 1326
  Options: (No TOS-capability, DC)
  LS Type: Network Links
  Link State ID: 10.7.89.77 (address of Designated Router)
  Advertising Router: 10.0.0.77
  LS Seq Number: 80000002
  Checksum: 0x99FA
  Length: 40
  Network Mask: /24
        Attached Router: 10.0.0.77
        Attached Router: 10.0.0.7
        Attached Router: 10.0.0.8
        Attached Router: 10.0.0.9

  Routing Bit Set on this LSA in topology Base with MTID 0
  LS age: 1333
  Options: (No TOS-capability, DC)
  LS Type: Network Links
  Link State ID: 10.10.11.11 (address of Designated Router)
  Advertising Router: 10.0.0.11
  LS Seq Number: 80000001
  Checksum: 0xCF02
  Length: 32
  Network Mask: /24
        Attached Router: 10.0.0.11
        Attached Router: 10.0.0.10

  Routing Bit Set on this LSA in topology Base with MTID 0
  LS age: 1330
  Options: (No TOS-capability, DC)
  LS Type: Network Links
  Link State ID: 10.11.110.110 (address of Designated Router)
  Advertising Router: 10.0.0.110
  LS Seq Number: 80000001
  Checksum: 0x380A
  Length: 32
  Network Mask: /24
        Attached Router: 10.0.0.110
        Attached Router: 10.0.0.11

R7#

'''
