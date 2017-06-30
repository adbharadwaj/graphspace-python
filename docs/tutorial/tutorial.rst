
Start here to begin working with `graphspace-python`.


Connecting to GraphSpace
------------------------
You can connect to GraphSpace using your username and password. You can also set the api host using the **set_api_host** method if you are using a different server.

>>> from graphspace_python.api.client import GraphSpace
>>> graphspace = GraphSpace('user1@example.com', 'user1')
>>> # graphspace.set_api_host('localhost:8000')


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
>>> G.set_is_public(1)
>>> graphspace.update_graph('My Sample Graph', graph=G)

Here is an another example.

>>> # Retrieving graph
>>> response = graphspace.get_graph(name) # You can retrieve a graph by id as well - graphspace.get_graph_by_id(id)
>>> graph = response.graph
>>> # Modifying the retrieved graph object
>>> graph.add_node('z', popup='sample node popup text', label='Z')
>>> graph.add_node_style('z', shape='ellipse', color='green', width=90, height=90)
>>> graph.set_is_public(1)
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

You can also delete your graph anytime using the **delete_graph** method.

>>> print graphspace.delete_graph('My Sample Graph')
Successfully deleted graph with id=39076
>>> assert graphspace.get_graph('My Sample Graph') is None


Creating a layout
-----------------

Create an empty layout with no nodes and no edges.

>>> from graphspace_python.graphs.classes.gslayout import GSLayout
>>> L = GSLayout()


Node Positions
--------------

You can set position of one node at a time.

>>> # Setting position of a node 'a' with y and x coordinates
>>> L.set_node_position('a', y=38.5, x=67.3)

>>> # Setting position of a node 'b' with y and x coordinates
>>> L.set_node_position('b', y=86, x=74.1)

Note: Setting position of an already present node updates its position.


Style
-----

You can also add style for a node or an edge.

>>> L.add_node_style('a', shape='ellipse', color='red', width=90, height=90)
>>> L.add_edge_style('a', 'b', directed=True, edge_style='dotted')


Layout Information
------------------
You can add more meaningful information about the layout like name, sharing status.

>>> L.set_name('My Sample Layout')
>>> L.set_is_shared(1)


Saving a layout on GraphSpace
-----------------------------
You can save your layout online using the **post_graph_layout** method.

>>> response = graphspace.post_graph_layout(graph_id=21722, layout=L)
>>> # layout_id = response.layout.layout_id


Fetching a layout from GraphSpace
---------------------------------

You can retrieve your saved layout anytime from GraphSpace using the **get_graph_layout** method.

>>> response = graphspace.get_graph_layout(graph_id=21722, layout_id=1068)
>>> layout = response.layout


Updating a layout on GraphSpace
-------------------------------
You can also update your layout anytime using the **update_graph_layout** method.

>>> L = GSLayout()
>>> L.set_node_position('x', y=38.5, x=67.3)
>>> L.set_node_position('y', y=86, x=74.1)
>>> L.add_node_style('y', shape='ellipse', color='red', width=90, height=90)
>>> L.add_edge_style('x', 'y', directed=True, edge_style='dotted')
>>> L.set_is_shared(0)
>>> graphspace.update_graph_layout(graph_id=21722, layout_id=1068, layout=L)

Here is an another example.

>>> # Retrieving layout
>>> response = graphspace.get_graph_graph_layout(graph_id=21722, layout_id=1068)
>>> layout = response.layout
>>> # Modifying the retrieved layout object
>>> layout.set_node_position('z', y=63, x=92)
>>> layout.add_node_style('z', shape='ellipse', color='green', width=90, height=90)
>>> layout.set_is_shared(0)
>>> # Updating layout
>>> graphspace.update_graph_layout(graph_id=21722, layout_id=1068, layout=layout)


Deleting a layout on GraphSpace
-------------------------------

You can also delete your layout anytime using the **delete_graph_layout** method.

>>> print graphspace.delete_graph_layout(graph_id=21722, layout_id=1068)
Successfully deleted layout with id=1068


Responses
---------

Responses from the API are parsed into Python objects.

**Graphs endpoint** responses are parsed into **GraphResponse** objects.

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

**Layouts endpoint** responses are parsed into **LayoutResponse** objects.

When response has a single layout object:

>>> response = graphspace.get_graph_layout(graph_id=21722, layout_id=1068)
>>> response.layout.name
u'My Sample Layout'

When response has multiple layout objects:

>>> response = graphspace.get_my_graph_layouts(graph_id=21722)
>>> response.layouts
[<Layout 1>, <Layout 2>, ...]
>>> response.total
4
>>> response.layouts[0].name
u'My Sample Layout'
