#!/usr/bin/env python

class Edge():
    '''Representation of an adjacency (source, destionation, cost)
    '''
    def __init__(self, src, dst, cost):
        self.src = src
        self.dst = dst
        self.cost = cost

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
