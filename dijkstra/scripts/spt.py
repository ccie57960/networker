#!/usr/bin/env python

from queue import PriorityQueue
from copy import deepcopy

class SPT():
    first_run = True
    '''SPF (Shortest Path Tree)
Based on a source (src) node/router. Find the best path to all nodes/routers
in the topology. Supports ECMP (Equal Cost MultiPath) thru the end-to-end'''

    def runSPT(self, src):
        '''Find the best path (including ECMP) to all nodes/routers
the output is stored withing the source instance (Node) database attribute

Example: Best path from src ("10.0.0.7") to "10.0.0.8" and "10.0.0.10" (ECMP):
-See the sample topology diagram

>>> nodes_dict[SOURCE].database[destinationX]
>>> nodes_dict["10.0.0.7"].database["10.0.0.8"]
{'cost': 10, 'tracepath': ['10.0.0.7', '10.0.0.8']}
>>>
>>> nodes_dict["10.0.0.7"].database["10.0.0.10"]
{'cost': 20, 'tracepath': [['10.0.0.7', '10.0.0.8', '10.0.0.10'], ['10.0.0.7', '10.0.0.9', '10.0.0.10']]}
'''
        pq = PriorityQueue()

        #Reset to default all internal attributes use for SFT computation (all instances)
        #Skipping the first run (every should be default)
        if self.first_run:
            self.first_run = False
        else:
            for i in src.all_instances:
                i.cost = float("inf")
                i.queued = False
                i.tracepath = []

        src.cost = 0
        src.tracepath.append(src.name)
        pq.put(src)

        while pq.qsize() > 0:
            current_node = pq.get()

            for edge in current_node.list_adjacency:
                new_cost = current_node.cost + edge.cost
                if new_cost == edge.dst.cost:
                    #ECMP - Equal Cost MultiPath
                    new_trace = []
                    new_trace = current_node.tracepath.copy()

                    #Create list of list (first case of ECMP only for this destionation)
                    if not isinstance(edge.dst.tracepath[0], list):
                        edge.dst.tracepath = [edge.dst.tracepath]
                    if isinstance(new_trace[0], list):
                        for a_trace in new_trace:
                            a_trace.append(edge.dst.name)
                            edge.dst.tracepath.append(a_trace.copy())
                    else:
                        new_trace.append(edge.dst.name)
                        edge.dst.tracepath.append(new_trace.copy())
                    src.database.update({edge.dst.name:{"cost":edge.dst.cost, "tracepath":edge.dst.tracepath}})

                elif new_cost < edge.dst.cost:
                    new_trace = []
                    edge.dst.cost = new_cost
                    new_trace = current_node.tracepath.copy()

                    if isinstance(new_trace[0], list):
                        new_trace = deepcopy(new_trace)
                        for index, a_trace in enumerate(new_trace):
                            a_trace.append(edge.dst.name)

                        edge.dst.tracepath = deepcopy(new_trace)
                    else:
                        new_trace.append(edge.dst.name)
                        edge.dst.tracepath = new_trace.copy()

                    src.database.update({edge.dst.name:{"cost":edge.dst.cost, "tracepath":edge.dst.tracepath}})

                    if edge.dst.queued == False:
                        pq.put(edge.dst)
                        edge.dst.queued == True
