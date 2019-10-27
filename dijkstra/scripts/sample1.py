#!/usr/bin/env python

from node import Node
from edge import Edge
from spt import SPT


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

ospf = SPT()
ospf.runSPT(r0)

print("From R0 to:\n")
print("Dst\tCost\tTracePath")

for k,v in r0.database.items():
    print(f'{k}\t{v["cost"]}\t{v["tracepath"]}')

# #Another way to do the same:
# lsdb = r0.return_database()
# for k,v in lsdb.items():
#     print(f'{k}\t{v["cost"]}\t{v["tracepath"]}')
