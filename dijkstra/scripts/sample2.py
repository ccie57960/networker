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
