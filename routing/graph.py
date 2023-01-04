#!/usr/bin/env python3

# Ailbhe Byrne

class Graph():

   def __init__(self):
      self.nodes = []     # list to store nodes (routers) in graph
      self.d_edges = {}   # dictionary to store edges (connections) in graph

# add node (router) to graph
   def addNode(self, name):
      self.nodes.append(name)   # add node to list

# add edge (connection) and weight (distance) to graph
   def addEdge(self, edge, weight):
      self.d_edges[edge] = weight   # add edge and weight to dictionary

# remove node (router) from graph
   def removeNode(self, name):
      self.nodes.remove(name)   # remove node from list
      for edge in list(self.d_edges.keys()):
         if name in edge:
            del self.d_edges[edge]   # remove all edges with node from dictionary

# remove edge (connection) and weight (distance) from graph
   def removeEdge(self, edge):
      for ek in list(self.d_edges.keys()):
         if edge == ek:
            del self.d_edges[edge]   # remove edge from dictionary
