#!/usr/bin/env python

class Node():
    all_instances = set() #Store all instances of this class
    #first_run = False

    def __init__(self, name, nickname = ""):
        '''Representation of a node/router
name: unique ID - IP Address (recommended)
nickname:optional name
queued: internal use (vary per SPT calculation)
list_adjacency: list of edge/object
cost: internal use (vary per SPT calculation)
tracepath: internal use (vary per SPT calculation)
database: SFT database (dictionary) using this instance/node as source
        '''
        self.name = name
        self.nickname = nickname
        self.queued = False
        self.list_adjacency = []
        self.cost = float("inf") #infinite initial cost
        self.tracepath = [] #from source to destination
        self.database = {}

        Node.all_instances.add(self)

    def __lt__(self, other):
        '''redifine "lt" or "<" for the sake of PriorityQueue'''
        return self.cost < other.cost

    def print_all_attributes(self):
            '''Print all attributes for this instance: -->str
            '''
            a_str = ""
            for k, v in self.__dict__.items():
                a_str += f"{k}:{v}\n"
            return a_str

    def return_attribute(self, attribute):
        '''return the value of any attribute of this instance: -->vary per attribute
        '''
        return self.__dict__.get(attribute)

    def return_database(self):
        '''return the database (SPT) for this instance -->dictionary
        '''
        return self.database

    def list_attributes(self):
        '''List all attribute of this instance: -->dict_keys
        '''
        return self.__dict__.keys()
