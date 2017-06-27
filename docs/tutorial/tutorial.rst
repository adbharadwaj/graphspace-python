
Start here to begin working with `graphspace-python`.


Creating a graph
----------------

Create an empty graph with no nodes and no edges.


>>> from graphspace_python.graphs.classes.gsgraph import GSGraph
>>> G = GSGraph()


Nodes
-----

You can add one node at a time.

>>> # Adding a node 'a' with a given popup and label
>>> G.add_node('a', popup='sample node popup text', label='A')
>>> # Adding style information for node 'a'
>>> G.add_node_style('a', shape='ellipse', color='red', width=90, height=90)


>>> # Adding a node 'b' with a given popup and label
>>> G.add_node('b', popup='sample node popup text', label='B')
>>> # Adding style information for node 'b'
>>> G.add_node_style('b', shape='ellipse', color='blue', width=40, height=40)


Edges
-----

You can also add one edge at a time using the **add_edge** method.

>>> G.add_edge('a', 'b', directed=True, popup='sample edge popup')
>>> G.add_edge_style('a', 'b', directed=True, edge_style='dotted')

Graph Information
-----------------
You can add more meaningful information about the graph like name, description and tags.

>>> G.set_name('My Sample Graph')
>>> G.set_data(data={
...     'description': 'my sample graph'
... })
>>> G.set_tags(['sample'])


Connecting to GraphSpace
------------------------
You can connect to GraphSpace using your username and password. You can also set the api host using the **set_api_host** method if you are using a different server.

>>> from graphspace_python.api.client import GraphSpace
>>> graphspace = GraphSpace('user1@example.com', 'user1')
>>> # graphspace.set_api_host('localhost:8000')

Saving a graph on GraphSpace
----------------------------
You can save your graph online using the **post_graph** method.

>>> graphspace.post_graph(G)


Fetching a graph from GraphSpace
--------------------------------

You can retrieve your saved graph anytime from GraphSpace using the **get_graph** method.

>>> response = graphspace.get_graph('My Sample Graph')
>>> graph = response.graph


Updating a graph on GraphSpace
------------------------------
You can also update your graph anytime using the **update_graph** method.

>>> G = GSGraph()
>>> G.add_node('a', popup='sample node popup text', label='A updated')
>>> G.add_node_style('a', shape='ellipse', color='green', width=90, height=90)
>>> G.add_node('b', popup='sample node popup text', label='B updated')
>>> G.add_node_style('b', shape='ellipse', color='yellow', width=40, height=40)
>>> G.add_edge('a', 'b', directed=True, popup='sample edge popup')
>>> G.add_edge_style('a', 'b', directed=True, edge_style='dotted')
>>> G.set_data(data={
...    'description': 'my sample graph'
... })
>>> graphspace.update_graph('My Sample Graph', graph=G, is_public=1)

Here is an another example.

>>> # Retrieving graph
>>> response = graphspace.get_graph(name) # You can retrieve a graph by id as well - graphspace.get_graph_by_id(id)
>>> graph = response.graph
>>> # Modifying the retrieved graph object
>>> graph.add_node('z', popup='sample node popup text', label='Z')
>>> graph.add_node_style('z', shape='ellipse', color='green', width=90, height=90)
>>> # Updating graph
>>> graphspace.update_graph('My Sample Graph', graph=graph)

Making a graph public on GraphSpace
-----------------------------------

You can also make a graph public using the **make_graph_public** method.

>>> graphspace.make_graph_public('My Sample Graph')
>>> assert graphspace.get_graph('My Sample Graph').graph.is_public == 1


Making a graph private on GraphSpace
------------------------------------

You can also make a graph private using the **make_graph_private** method.

>>> graphspace.make_graph_private('My Sample Graph')
>>> assert graphspace.get_graph('My Sample Graph').graph.is_public == 0


Deleting a graph on GraphSpace
------------------------------

You can also delete your graph anytime using the **update_graph** method.

>>> print graphspace.delete_graph('My Sample Graph')
Successfully deleted graph with id=39076
>>> assert graphspace.get_graph('My Sample Graph') is None


Responses
---------

Responses from the API are parsed into Python objects.

Graphs endpoint responses are parsed into **GraphResponse** objects.

When response has a single graph object:

>>> response = graphspace.get_graph('My Sample Graph')
>>> response.graph.name
u'My Sample Graph'

When response has multiple graph objects:

>>> response = graphspace.get_my_graphs()
>>> response.graphs
[<Graph 1>, <Graph 2>, ...]
>>> response.total
32
>>> response.graphs[0].name
u'My Sample Graph'
