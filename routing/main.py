#!/usr/bin/env python3

import uvicorn
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI
from graph import Graph
from shortest_path import get_shortest_path

api_desc = '''
   ### Ailbhe Byrne

   This is a webservice using FastAPI that consists of 5 endpoints, which send and receive JSON data. It is used to represent routers in a network
   by using nodes on a graph: routers and connections can be added and removed, and the shortest path between them can be found.
'''

tags_metadata = [
   {
      "name": "Add Router",
      "description": "Adds a router to the network",
   },
   {
      "name": "Add Connection",
      "description": "Adds a connection between two routers to the network",
   },
   {
      "name": "Remove Router",
      "description": "Removes a router from the network, along with all its connections",
   },
   {
      "name": "Remove Connection",
      "description": "Removes a connection between two routers from the network",
   },
   {
      "name": "Shortest Path",
      "description": "Finds the shortest path between two routers on the network",
   },
]

# class for router with name
class Router(BaseModel):
   name: str

# class for connections between routers
class Connection(BaseModel):
   from_: str = Field(None, alias="from")
   to: str
   weight: Optional[int] = None

app = FastAPI(
   title="CA304 Networks 2: Assignment 2",
   description=api_desc,
   openapi_tags=tags_metadata
   )

graph = Graph()

add_router_desc = '''
   The input is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "name": "string"  
   }  
   The string for name represents the name of the router to be added, which should be a letter of the alphabet.

   The output is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "status": "string"  
   }  
   The string for status will contain a message letting the user know whether adding the router succeeded
   or if the router already existed in the network.

   **Example input:**  
   {  
   &nbsp;&nbsp; "name": "A"  
   }

   **Example output (success):**  
   {  
   &nbsp;&nbsp; "status": "success"  
   }

   **Example output (already exists):**  
   {  
   &nbsp;&nbsp; "status": "Error, node already exists"  
   }
'''

# add router to graph
@app.post("/addrouter/", tags=["Add Router"], description=add_router_desc)
async def add_node_to_graph(router: Router):
   router = router.dict()
   name = router["name"]
   if name in graph.nodes:   # if router already in graph
      return {
               "status": "Error, node already exists"
             }
   else:
      graph.addNode(name)    # if router not in graph, add to graph
      return {
               "status": "success"
             }

add_connection_desc = '''
   The input is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "from": "string",  
   &nbsp;&nbsp; "to": "string",  
   &nbsp;&nbsp; "weight": integer  
   }  
   The string for from represents the name of one of the routers in the connection, which should be a letter of the alphabet.  
   The string for to represents the name of the other router in the connection, which should also be a letter of the alphabet.  
   The integer for weight represents the weight of the connection between the two routers.

   The output is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "status": "string"  
   }  
   The string for status will contain a message letting the user know whether adding the connection between the routers succeeded,
   whether the weight for the connection was updated or if one or both of the routers does not exist.

   **Example input:**  
   {  
   &nbsp;&nbsp; "from": "A",  
   &nbsp;&nbsp; "to": "B",  
   &nbsp;&nbsp; "weight": 7  
   }  

   **Example output (success):**  
   {  
   &nbsp;&nbsp; "status": "success"  
   }

   **Example output (updated):**  
   {  
   &nbsp;&nbsp; "status": "updated"  
   }

   **Example output (don't exist):**  
   {  
   &nbsp;&nbsp; "status": "Error, router does not exist"  
   }
'''

# add connection between routers to graph
@app.post("/connect/", tags=["Add Connection"], description=add_connection_desc)
async def add_edge_to_graph(connection: Connection):
   connection = connection.dict()
   from_, to, weight = connection["from_"], connection["to"], connection["weight"]
   edge = "".join(sorted(from_ + to))                      # add from and to routers for connection and sort alphabetically
   if from_ not in graph.nodes or to not in graph.nodes:   # if from or to routers not in graph
      return {
               "status": "Error, router does not exist"
             }
   elif edge in graph.d_edges:        # if connection already in graph
      graph.addEdge(edge, weight)     # update connection weight
      return {
               "status": "updated"
             }
   else:                              # if connection not in graph
      graph.addEdge(edge, weight)     # add connection and weight to graph
      return {
               "status": "success"
             }

remove_router_desc = '''
   The input is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "name": "string"  
   }  
   The string for name represents the name of the router to be removed, which should be a letter of the alphabet.

   The output is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "status": "string"  
   }  
   The string for status will contain a message letting the user know whether removing the router succeeded.

   **Example input:**  
   {  
   &nbsp;&nbsp; "name": "A"  
   }

   **Example output:**  
   {  
   &nbsp;&nbsp; "status": "success"  
   }
'''

# remove router from graph
@app.post("/removerouter/", tags=["Remove Router"], description=remove_router_desc)
async def remove_node_from_graph(router: Router):
   router = router.dict()
   name = router["name"]
   if name in graph.nodes:     # if router in graph
      graph.removeNode(name)   # remove router from graph
   return {
            "status":"success"
          }

remove_connection_desc = '''
   The input is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "from": "string",  
   &nbsp;&nbsp; "to": "string"  
   }  
   The string for from represents the name of one of the routers in the connection, which should be a letter of the alphabet.  
   The string for to represents the name of the other router in the connection, which should also be a letter of the alphabet.  

   The output is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "status": "string"  
   }  
   The string for status will contain a message letting the user know whether removing the connection between the routers succeeded.

   **Example input:**  
   {  
   &nbsp;&nbsp; "from": "A",  
   &nbsp;&nbsp; "to": "B"  
   }  

   **Example output:**  
   {  
   &nbsp;&nbsp; "status": "success"  
   }
'''

# remove connection between routers from graph
@app.post("/removeconnection/", tags=["Remove Connection"], description=remove_connection_desc)
async def remove_edge_from_graph(connection: Connection):
   connection = connection.dict()
   from_, to = connection["from_"], connection["to"]
   edge = "".join(sorted(from_ + to))   # add from and to routers for connection and sort alphabetically
   if edge in graph.d_edges:            # if connection in graph
      graph.removeEdge(edge)            # remove connection
   return {
            "status":"success"
          }

shortest_path_desc = '''
   The input is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "from": "string",  
   &nbsp;&nbsp; "to": "string"  
   }  
   The string for from represents the name of the first router in the path, which should be a letter of the alphabet.  
   The string for to represents the name of the target router in the path, which should also be a letter of the alphabet.  

   The output is JSON data in the form of:  
   {  
   &nbsp;&nbsp; "from": "string",  
   &nbsp;&nbsp; "to": "string",  
   &nbsp;&nbsp; "weight": integer,  
   &nbsp;&nbsp; "route": list  
   }  
   The string for from will contain the name of the first router in the path.  
   The string for to will contain the name of the target router in the path.  
   The integer for weight will contain the total weight of the shortest path between the two routers.  
   The list for route will contain a list of all the connections and weights in the shortest path between the two routers.  

   **Example input:**  
   {  
   &nbsp;&nbsp; "from": "A",  
   &nbsp;&nbsp; "to": "F"  
   }  

   **Example output (route exists):**  
   {  
   &nbsp;&nbsp; "from": "A",  
   &nbsp;&nbsp; "to": "F",  
   &nbsp;&nbsp; "weight": 20,  
   &nbsp;&nbsp; "route": [  
   &nbsp;&nbsp;&nbsp;&nbsp; {  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "from": "A",  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "to": "C",  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "weight": 9  
   &nbsp;&nbsp;&nbsp;&nbsp; },  
   &nbsp;&nbsp;&nbsp;&nbsp; {  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "from": "C",  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "to": "E",  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "weight": 2  
   &nbsp;&nbsp;&nbsp;&nbsp; },  
   &nbsp;&nbsp;&nbsp;&nbsp; {  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "from": "E",  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "to": "F",  
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "weight": 9  
   &nbsp;&nbsp;&nbsp;&nbsp; }  
   &nbsp;&nbsp; ]  
   }  

   **Example output (route does not exist):**  
   {  
   &nbsp;&nbsp; "from": "A",  
   &nbsp;&nbsp; "to": "F",  
   &nbsp;&nbsp; "weight": -1,  
   &nbsp;&nbsp; "route": []  
   }

   **Example output (from and to are same):**  
   {  
   &nbsp;&nbsp; "from": "A",  
   &nbsp;&nbsp; "to": "A",  
   &nbsp;&nbsp; "weight": 0,  
   &nbsp;&nbsp; "route": [  
   &nbsp;&nbsp;&nbsp;&nbsp; "A"  
   &nbsp;&nbsp; ]  
   }
'''

# get shortest path between 2 routers
@app.post("/route/", tags=["Shortest Path"], description=shortest_path_desc)
async def shortest_path(connection: Connection):
   connection = connection.dict()
   from_, to = connection["from_"], connection["to"]
   if from_ == to:               # if from router is same as to router
      if from_ in graph.nodes:   # if router is in graph
         total_weight = 0
         route = [from_]
      else:                      # if router not in graph
         total_weight = -1
         route = []
   else:                         # if from router not same as to router
      route = []
      if graph.d_edges != {}:    # if graph has connections
         path = get_shortest_path(graph.nodes, graph.d_edges, from_, to)   # get shortest path between routers
         if path != None:                       # if a path exists between from and to routers
            path_edges = get_path_edges(path)   # get connections in path
            total_weight = sum([graph.d_edges["".join(sorted(edge))] for edge in path_edges])   # get total weight of path (add connection weights)
            for edge in path_edges:
               route.append({"from": edge[0], "to": edge[1], "weight": graph.d_edges["".join(sorted(edge))]})   # add connections and weights to route
         else:
            total_weight = -1   # if a path does not exist
      else:
         total_weight = -1      # path does not exist in graph with no connections
   return {
            "from": from_,
            "to": to,
            "weight": total_weight,
            "route": route,
          }

# get connections in path between routers
def get_path_edges(path):
   path_edges = []
   for i in range(len(path) - 1):
      path_edges.append(path[i] + path[i + 1])   # split path string up into connections and add to list
   return path_edges


# server will also run in terminal with "python3 main.py"
def main():
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == '__main__':
   main()
