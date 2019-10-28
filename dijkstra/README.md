# dijkstra

This is my implementation of Dijkstra SPT (Shortest Path Tree).

Based on a "source" (node/router) it calculates the SPT to each node in the topology.

The plan is to practice (scripting, network automation).
Feel free to use, modify, share it. Any feedback would be appreciated :D

Lets explain the two examples in the documentation directory.

### Sample#1

This example is for illustration purpose, the next one is the practical one. The first diagram represents the original topology, the second one is the result after running the SPT using **R0 as source** of the tree. Note: the code doesn't create this graph.

![SampleTopology1](https://raw.githubusercontent.com/ccie57960/networker/master/dijkstra/documentation/SampleTopology1.png)

The code will return the database (SPT) as dictionary via some methods, here a representation for illustration purpose:

peter@pc:~/git/networker/dijkstra/scripts$ Python3.6 sample1.py
```Python
From R0 to:

Dst	Cost	TracePath
R8	14	[['R0', 'R8'], ['R0', 'R7', 'R6', 'R8'], ['R0', 'R1', 'R2', 'R8']]
R1	4	['R0', 'R1']
R7	8	['R0', 'R7']
R2	12	['R0', 'R1', 'R2']
R6	9	['R0', 'R7', 'R6']
R5	11	['R0', 'R7', 'R6', 'R5']
R3	19	['R0', 'R1', 'R2', 'R3']
R4	21	['R0', 'R7', 'R6', 'R5', 'R4']
```

Now that you have an high level view let's go more in detail. There are three classes to represent the main components:
+ **node**: representation of a node/router, the constructor needs a name (unique IP Address or loopback address is recommended), you could also include additional name (ie: hostname). Use the Python "help" option for more details.

+ **edge**: representation of an logical adjacency between two nodes (link), the constructor needs the source node instance, destination node instance and cost/metric (src, dst, cost). Use the Python "help" option for more details.

+ **spt**: representation of Dijkstra algorithm, the constructor needs the source node instance. Use the Python "help" option for more details.

For each class I included some methods to access the attribute of each class, ie: ```node.return_database()``` will return the SPT (dictionary) for the respective node instance.


Here is the code that returned the previous output:
```Python
from node import Node
from edge import Edge
from spt import SPT

#Create all nodes/routers
r0 = Node("R0")
r1 = Node("R1")
r2 = Node("R2")
r3 = Node("R3")
r4 = Node("R4")
r5 = Node("R5")
r6 = Node("R6")
r7 = Node("R7")
r8 = Node("R8")

list_r = [r0,r1,r2,r3,r4,r5,r6,r7,r8]

#Create all edges/links
e01 = Edge(r0,r1,4)
e10 = Edge(r1,r0,4)
e07 = Edge(r0,r7,8)
e70 = Edge(r7,r0,8)

e12 = Edge(r1,r2,8)
e21 = Edge(r1,r2,8)
e17 = Edge(r1,r7,11)
e71 = Edge(r7,r1,11)

e78 = Edge(r7,r8,7)
e87 = Edge(r8,r7,7)
e76 = Edge(r7,r6,1)
e67 = Edge(r6,r7,1)

e28 = Edge(r2,r8,2)
e82 = Edge(r8,r2,2)
e23 = Edge(r2,r3,7)
e32 = Edge(r3,r2,7)
e25 = Edge(r2,r5,4)
e52 = Edge(r5,r2,4)

e86 = Edge(r8,r6,6)
e68 = Edge(r6,r8,6)

e65 = Edge(r6,r5,2)
e56 = Edge(r5,r6,2)

e53 = Edge(r5,r3,14)
e35 = Edge(r3,r5,14)
e54 = Edge(r5,r4,10)
e45 = Edge(r4,r5,10)

e34 = Edge(r3,r4,9)
e43 = Edge(r4,r3,9)

#<ECMP_Test>
e86 = Edge(r8,r6,5)
e68 = Edge(r6,r8,5)
e08 = Edge(r0,r8,14)
e80 = Edge(r8,r0,14)
r0.list_adjacency.append(e08)
r8.list_adjacency.append(e80)
#</ECMP_Test>

#Assign the edge to each node
r0.list_adjacency.append(e01)
r0.list_adjacency.append(e07)

r1.list_adjacency.append(e10)
r1.list_adjacency.append(e12)
r1.list_adjacency.append(e17)

r2.list_adjacency.append(e21)
r2.list_adjacency.append(e23)
r2.list_adjacency.append(e25)
r2.list_adjacency.append(e28)

r3.list_adjacency.append(e32)
r3.list_adjacency.append(e34)
r3.list_adjacency.append(e35)

r4.list_adjacency.append(e43)
r4.list_adjacency.append(e45)

r5.list_adjacency.append(e52)
r5.list_adjacency.append(e53)
r5.list_adjacency.append(e54)
r5.list_adjacency.append(e56)

r6.list_adjacency.append(e65)
r6.list_adjacency.append(e67)
r6.list_adjacency.append(e68)

r7.list_adjacency.append(e70)
r7.list_adjacency.append(e71)
r7.list_adjacency.append(e76)
r7.list_adjacency.append(e78)

r8.list_adjacency.append(e82)
r8.list_adjacency.append(e86)
r8.list_adjacency.append(e87)

#Create SPT instance
net_spt = SPT()
#Run SFT for R0 as the source of the tree
net_spt.runSPT(r0)

print("From R0 to:\n")
print("Dst\tCost\tTracePath")

lsdb = r0.return_database()
for k,v in lsdb.items():
    print(f'{k}\t{v["cost"]}\t{v["tracepath"]}')

# #Another way to do the same:
# for k,v in r0.database.items():
#     print(f'{k}\t{v["cost"]}\t{v["tracepath"]}')
```


### Sample#2

This is a more practical example.
The diagram represents the original topology Note: the code doesn't create this graph.

![SampleTopology2](https://raw.githubusercontent.com/ccie57960/networker/master/dijkstra/documentation/SampleTopology2.png)

Notes:
+ All routers are running Cisco IOS.
+ OSPF process 1 and area 0
+ OSPF multi-access interfaces:
 + All connected to L2SW
 + R10 to/from R11 edge/link
+ All other interfaces are OSPF point-to-point
+ Looback: 10.0.0.X, where X=router number, ie:
 + "R7":"10.0.0.7"
 + "R120":"10.0.0.120"
+ I used the networker library for simplicity. [Click here to read this library documentation](https://github.com/ccie57960/networker/blob/master/networker_methods/README.md). **It highly recommended to read this documentation before continue**.
+ I used some methods from the "[networker library](https://github.com/ccie57960/networker/blob/master/networker_methods/README.md)" to get and parse the OSPF database information from the routers. I did some trick (copy&paste instead of SSH client), in real life you may use a SSH client (Napalm or Netmiko) then parse the information using the [networker library](https://github.com/ccie57960/networker/blob/master/networker_methods/README.md) or anything you prefer like: Netconf, Resconf, gRPC, etc.

### Sample#2 Output: SPT from each router/node:
```Python
peter@pc:~/git/networker/dijkstra/scripts$ python3.6 sample2.py
==================================================
10.0.0.7 SPT:
10.0.0.77	10	['10.0.0.7', '10.0.0.77']
10.0.0.8	10	['10.0.0.7', '10.0.0.8']
10.0.0.9	10	['10.0.0.7', '10.0.0.9']
10.0.0.10	20	[['10.0.0.7', '10.0.0.8', '10.0.0.10'], ['10.0.0.7', '10.0.0.9', '10.0.0.10']]
10.0.0.12	20	['10.0.0.7', '10.0.0.8', '10.0.0.12']
10.0.0.11	30	[['10.0.0.7', '10.0.0.8', '10.0.0.10', '10.0.0.11'], ['10.0.0.7', '10.0.0.9', '10.0.0.10', '10.0.0.11']]
10.0.0.120	30	['10.0.0.7', '10.0.0.8', '10.0.0.12', '10.0.0.120']
10.0.0.110	40	[['10.0.0.7', '10.0.0.8', '10.0.0.10', '10.0.0.11', '10.0.0.110'], ['10.0.0.7', '10.0.0.9', '10.0.0.10', '10.0.0.11', '10.0.0.110'], ['10.0.0.7', '10.0.0.8', '10.0.0.12', '10.0.0.120', '10.0.0.110']]
==================================================
10.0.0.8 SPT:
10.0.0.10	10	['10.0.0.8', '10.0.0.10']
10.0.0.12	10	['10.0.0.8', '10.0.0.12']
10.0.0.9	10	['10.0.0.8', '10.0.0.9']
10.0.0.77	10	['10.0.0.8', '10.0.0.77']
10.0.0.7	10	['10.0.0.8', '10.0.0.7']
10.0.0.11	20	['10.0.0.8', '10.0.0.10', '10.0.0.11']
10.0.0.120	20	['10.0.0.8', '10.0.0.12', '10.0.0.120']
10.0.0.110	30	[['10.0.0.8', '10.0.0.10', '10.0.0.11', '10.0.0.110'], ['10.0.0.8', '10.0.0.12', '10.0.0.120', '10.0.0.110']]
==================================================
10.0.0.9 SPT:
10.0.0.10	10	['10.0.0.9', '10.0.0.10']
10.0.0.8	10	['10.0.0.9', '10.0.0.8']
10.0.0.77	10	['10.0.0.9', '10.0.0.77']
10.0.0.7	10	['10.0.0.9', '10.0.0.7']
10.0.0.11	20	['10.0.0.9', '10.0.0.10', '10.0.0.11']
10.0.0.12	20	['10.0.0.9', '10.0.0.8', '10.0.0.12']
10.0.0.110	30	['10.0.0.9', '10.0.0.10', '10.0.0.11', '10.0.0.110']
10.0.0.120	30	['10.0.0.9', '10.0.0.8', '10.0.0.12', '10.0.0.120']
==================================================
10.0.0.10 SPT:
10.0.0.8	10	['10.0.0.10', '10.0.0.8']
10.0.0.9	10	['10.0.0.10', '10.0.0.9']
10.0.0.11	10	['10.0.0.10', '10.0.0.11']
10.0.0.12	20	['10.0.0.10', '10.0.0.8', '10.0.0.12']
10.0.0.77	20	[['10.0.0.10', '10.0.0.8', '10.0.0.77'], ['10.0.0.10', '10.0.0.9', '10.0.0.77']]
10.0.0.7	20	[['10.0.0.10', '10.0.0.8', '10.0.0.7'], ['10.0.0.10', '10.0.0.9', '10.0.0.7']]
10.0.0.110	20	['10.0.0.10', '10.0.0.11', '10.0.0.110']
10.0.0.120	30	[['10.0.0.10', '10.0.0.8', '10.0.0.12', '10.0.0.120'], ['10.0.0.10', '10.0.0.11', '10.0.0.110', '10.0.0.120']]
==================================================
10.0.0.11 SPT:
10.0.0.110	10	['10.0.0.11', '10.0.0.110']
10.0.0.10	10	['10.0.0.11', '10.0.0.10']
10.0.0.120	20	['10.0.0.11', '10.0.0.110', '10.0.0.120']
10.0.0.8	20	['10.0.0.11', '10.0.0.10', '10.0.0.8']
10.0.0.9	20	['10.0.0.11', '10.0.0.10', '10.0.0.9']
10.0.0.12	30	[['10.0.0.11', '10.0.0.110', '10.0.0.120', '10.0.0.12'], ['10.0.0.11', '10.0.0.10', '10.0.0.8', '10.0.0.12']]
10.0.0.77	30	[['10.0.0.11', '10.0.0.10', '10.0.0.8', '10.0.0.77'], ['10.0.0.11', '10.0.0.10', '10.0.0.9', '10.0.0.77']]
10.0.0.7	30	[['10.0.0.11', '10.0.0.10', '10.0.0.8', '10.0.0.7'], ['10.0.0.11', '10.0.0.10', '10.0.0.9', '10.0.0.7']]
==================================================
10.0.0.12 SPT:
10.0.0.8	10	['10.0.0.12', '10.0.0.8']
10.0.0.120	10	['10.0.0.12', '10.0.0.120']
10.0.0.10	20	['10.0.0.12', '10.0.0.8', '10.0.0.10']
10.0.0.9	20	['10.0.0.12', '10.0.0.8', '10.0.0.9']
10.0.0.77	20	['10.0.0.12', '10.0.0.8', '10.0.0.77']
10.0.0.7	20	['10.0.0.12', '10.0.0.8', '10.0.0.7']
10.0.0.110	20	['10.0.0.12', '10.0.0.120', '10.0.0.110']
10.0.0.11	30	[['10.0.0.12', '10.0.0.120', '10.0.0.110', '10.0.0.11'], ['10.0.0.12', '10.0.0.8', '10.0.0.10', '10.0.0.11']]
==================================================
10.0.0.77 SPT:
10.0.0.7	10	['10.0.0.77', '10.0.0.7']
10.0.0.8	10	['10.0.0.77', '10.0.0.8']
10.0.0.9	10	['10.0.0.77', '10.0.0.9']
10.0.0.10	20	[['10.0.0.77', '10.0.0.8', '10.0.0.10'], ['10.0.0.77', '10.0.0.9', '10.0.0.10']]
10.0.0.12	20	['10.0.0.77', '10.0.0.8', '10.0.0.12']
10.0.0.11	30	[['10.0.0.77', '10.0.0.8', '10.0.0.10', '10.0.0.11'], ['10.0.0.77', '10.0.0.9', '10.0.0.10', '10.0.0.11']]
10.0.0.120	30	['10.0.0.77', '10.0.0.8', '10.0.0.12', '10.0.0.120']
10.0.0.110	40	[['10.0.0.77', '10.0.0.8', '10.0.0.10', '10.0.0.11', '10.0.0.110'], ['10.0.0.77', '10.0.0.9', '10.0.0.10', '10.0.0.11', '10.0.0.110'], ['10.0.0.77', '10.0.0.8', '10.0.0.12', '10.0.0.120', '10.0.0.110']]
==================================================
10.0.0.110 SPT:
10.0.0.120	10	['10.0.0.110', '10.0.0.120']
10.0.0.11	10	['10.0.0.110', '10.0.0.11']
10.0.0.12	20	['10.0.0.110', '10.0.0.120', '10.0.0.12']
10.0.0.10	20	['10.0.0.110', '10.0.0.11', '10.0.0.10']
10.0.0.8	30	[['10.0.0.110', '10.0.0.120', '10.0.0.12', '10.0.0.8'], ['10.0.0.110', '10.0.0.11', '10.0.0.10', '10.0.0.8']]
10.0.0.9	30	['10.0.0.110', '10.0.0.11', '10.0.0.10', '10.0.0.9']
10.0.0.77	40	[['10.0.0.110', '10.0.0.120', '10.0.0.12', '10.0.0.8', '10.0.0.77'], ['10.0.0.110', '10.0.0.11', '10.0.0.10', '10.0.0.8', '10.0.0.77'], ['10.0.0.110', '10.0.0.11', '10.0.0.10', '10.0.0.9', '10.0.0.77']]
10.0.0.7	40	[['10.0.0.110', '10.0.0.120', '10.0.0.12', '10.0.0.8', '10.0.0.7'], ['10.0.0.110', '10.0.0.11', '10.0.0.10', '10.0.0.8', '10.0.0.7'], ['10.0.0.110', '10.0.0.11', '10.0.0.10', '10.0.0.9', '10.0.0.7']]
==================================================
10.0.0.120 SPT:
10.0.0.110	10	['10.0.0.120', '10.0.0.110']
10.0.0.12	10	['10.0.0.120', '10.0.0.12']
10.0.0.11	20	['10.0.0.120', '10.0.0.110', '10.0.0.11']
10.0.0.8	20	['10.0.0.120', '10.0.0.12', '10.0.0.8']
10.0.0.10	30	[['10.0.0.120', '10.0.0.110', '10.0.0.11', '10.0.0.10'], ['10.0.0.120', '10.0.0.12', '10.0.0.8', '10.0.0.10']]
10.0.0.9	30	['10.0.0.120', '10.0.0.12', '10.0.0.8', '10.0.0.9']
10.0.0.77	30	['10.0.0.120', '10.0.0.12', '10.0.0.8', '10.0.0.77']
10.0.0.7	30	['10.0.0.120', '10.0.0.12', '10.0.0.8', '10.0.0.7']

```

### Sample#2 Code:
```Python
#!/usr/bin/env python

from node import Node
from edge import Edge
from spt import SPT
import networker

#For simplicity sake. In real life you may use an SSH client like Napalm or Netmiko
#output from: show ip ospf 1 0 database router
sh_lsa1 = networker.sh_lsa1()
#output from: show ip ospf 1 0 database network
sh_lsa2 = networker.sh_lsa2()
ospf = SPT()

#Parse the raw output (from IOS router)
dict_lsa2 = networker.ios_ospf_lsa2(sh_lsa2)
dict_lsa1 = networker.ios_ospf_lsa1(sh_lsa1, dict_lsa2)

list_routers = dict_lsa1.keys()

dict_routers = {}
list_edges = []
#Create nodes/routers
for router in list_routers:
    dict_routers.update({router:Node(router)})

#Create Edges/Adjacencies
for router, neighbors in dict_lsa1.items():
    for a_neighbor, list_metric in neighbors.items():
        uniq_metrics = set(list_metric)
        for a_metric in uniq_metrics:
            list_edges.append(Edge(dict_routers[router], dict_routers[a_neighbor], a_metric))

#Assign Edge to each node
for edge in list_edges:
    edge.src.list_adjacency.append(edge)

for a_router in dict_routers.keys():
    print("=" *50)
    print(f"{a_router} SPT:")
    ospf.runSPT(dict_routers[a_router])
    for k,v in dict_routers[a_router].database.items():
        print(f'{k}\t{v["cost"]}\t{v["tracepath"]}')
```

Feel free to use, modify, share it. Any feedback would be appreciated :D Also you could optionally donate (https://www.paypal.me/57960)

Hope this may help you.
