#!/usr/bin/env python3

# Ailbhe Byrne

# reference (did not directly copy): https://github.com/mburst/dijkstras-algorithm/blob/master/dijkstras.py
# get shortest path between routers (nodes in a graph)
def get_shortest_path(nodes, edges, from_, to):
   path = {}               # keep track of path to target (to router)

   unvisited = {}          # keep track of unvisited nodes
   unvisited[from_] = 0    # from router is distance of 0

   total_dist = {}         # keep track of total distance to nodes
   total_dist[from_] = 0   # from router is distance of 0
   
   for n in nodes:
      if n not in unvisited:
         total_dist[n] = float("inf")   # set distance to other nodes as infinity
         unvisited[n] = float("inf")    # set distance to other nodes as infinity
      path[n] = None                    # set path of all nodes as none

   while unvisited != {}:
      min_dist_node = min(unvisited.items(), key=sort_on)[0]   # get node in unvisited with shortest distance
      del unvisited[min_dist_node]                             # remove current node from unvisited

      if min_dist_node == to:     # if current node is target (to)
         path_str = ""                  # create a string for path to target
         while min_dist_node != None:   # while not at target (to) in path
            path_str += min_dist_node   # add previous node to path
            min_dist_node = path[min_dist_node]   # follow path of previous nodes to get shortest path
         return path_str[::-1]                    # reverse string to get path from 'from' router to 'to' router

      if total_dist[min_dist_node] == float("inf"):   # if distance to current node is infinity
         break

      neighbours = get_neighbours(min_dist_node, edges)   # get neighbours of current node
      for neighbour in neighbours:
         new_dist = total_dist[min_dist_node] + neighbours[neighbour]   # get distance to neighbour node through current node
         if new_dist < total_dist[neighbour]:    # if this distance is less than total distance to neighbour
            total_dist[neighbour] = new_dist     # set new total distance of neighbour
            path[neighbour] = min_dist_node      # add neighbour to path with current node as previous node
            unvisited[neighbour] = new_dist      # add neighbour to unvisited with new distance
   return None   # if path does not exist return none

# return 2nd item in tuple (distance/weight of connection)
def sort_on(tuple):
   return tuple[1]

# get neighbours of node i.e. routers with connection to current router in graph
def get_neighbours(node, edges):
   neighbours = {}
   for edge in edges.keys():   # for each connection
      if node in edge:         # if current router is in connection
         n = edge.replace(node, "")    # get router current router is connected to (replace current router with "")
         neighbours[n] = edges[edge]   # add router and distance (weight) to neighbours
   return neighbours
