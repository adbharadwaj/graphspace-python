
Start here to begin working with `graphspace-python`.


Creating a graph
----------------

Create an empty graph with no nodes and no edges.


>>> from graphspace_python.graphs.classes.gsgraph import GSGraph
>>> G = GSGraph()


Adding nodes
------------

>>> G.add_node('a', popup='sample node popup text', label='A')
>>> G.add_node_style('a', shape='ellipse', color='red', width=90, height=90)



>>> G.add_node('b', popup='sample node popup text', label='B')
>>> G.add_node_style('b', shape='ellipse', color='blue', width=40, height=40)


Adding edges
------------


>>> G.add_edge('a', 'b', directed=True, popup='sample edge popup')
>>> G.add_edge_style('a', 'b', directed=True, edge_style='dotted')

Connecting to GraphSpace
------------------------

>>> graphspace = GraphSpace('user1@example.com', 'user1')
>>> # graphspace.set_api_host('localhost:8000') 

Saving a graph on GraphSpace
----------------------------

>>> G.set_name('My Sample Graph')
>>> G.set_data(data={
...     'description': 'my sample graph'
... })
>>> G.set_tags(['sample'])
>>> print graphspace.post_graph(G)


Fetching a graph from GraphSpace
--------------------------------

>>> print graphspace.get_graph('My Sample Graph')

Updating a graph on GraphSpace
------------------------------

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


>>> graphspace.update_graph('My Sample Graph', graph=graph1, is_public=1)


Deleting a graph on GraphSpace
------------------------------

Making a graph public on GraphSpace
-----------------------------------

Making a graph private on GraphSpace
------------------------------------
