#!/usr/bin/env python

from node import Node
from edge import Edge
from spt import SPT
import networker


sh_lsa1 = networker.sh_lsa1()
sh_lsa2 = networker.sh_lsa2()
ospf = SPT()

dict_lsa2 = networker.ios_ospf_lsa2(sh_lsa2)
dict_lsa1 = networker.ios_ospf_lsa1(sh_lsa1, dict_lsa2)

list_routers = dict_lsa1.keys()

dict_routers = {}
list_edges = []
#Create nodes/routers
for router in list_routers:
    dict_routers.update({router:Node(router)})

#Create Edge/Adjacencies
for router, neighbors in dict_lsa1.items():
    for a_neighbor, list_metric in neighbors.items():
        uniq_metrics = set(list_metric)
        for a_metric in uniq_metrics:
            list_edges.append(Edge(dict_routers[router], dict_routers[a_neighbor], a_metric))

#Asigned Edge to each node
for edge in list_edges:
    edge.src.list_adjacency.append(edge)

# ospf.runSPT(dict_routers["10.0.0.7"])


for a_router in dict_routers.keys():
    print("=" *50)
    print(f"{a_router} SFT:")
    ospf.runSPT(dict_routers[a_router])
    for k,v in dict_routers[a_router].database.items():
        print(f'{k}\t{v["cost"]}\t{v["tracepath"]}')
