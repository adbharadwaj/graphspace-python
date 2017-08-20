import json
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Initialize graph
G = GSGraph()
# Set name, tags and visibility status
G.set_name('Pie Style')
G.set_tags(['pie-style', 'pie', 'graphspace', 'demo'])
G.set_is_public()
# Define and set data
data = {
    'description': 'A demo network where the nodes constitute of pie charts.<br>You can also view this demo graph at:\
 <a href=\"http://js.cytoscape.org/demos/pie-style/\">http://js.cytoscape.org/demos/pie-style/</a>',
    'directed': True
}
G.set_data(data)

# Construct nodes and edges of the graph
# Add nodes
G.add_node('a', {"foo": 3, "bar": 5, "baz": 2})
G.add_node('b', {"foo": 6, "bar": 1, "baz": 3})
G.add_node('c', {"foo": 2, "bar": 3, "baz": 5})
G.add_node('d', {"foo": 7, "bar": 1, "baz": 2})
G.add_node('e', {"foo": 2, "bar": 3, "baz": 5})
# Set node positions
G.set_node_position('a', y=60, x=550.5)
G.set_node_position('b', y=193.2, x=733.8)
G.set_node_position('c', y=408.6, x=663.8)
G.set_node_position('d', y=408.6, x=437.2)
G.set_node_position('e', y=193.2, x=367.2)
# Add edges
G.add_edge('a', 'e', {'weight': 1})
G.add_edge('a', 'b', {'weight': 3})
G.add_edge('b', 'e', {'weight': 4})
G.add_edge('b', 'c', {'weight': 5})
G.add_edge('c', 'e', {'weight': 6})
G.add_edge('c', 'd', {'weight': 2})
G.add_edge('d', 'e', {'weight': 7})

# You can also construct the nodes and edges of the graph by loading the graph.json
# file and setting it for the graph.

# with open('graph.json') as graph_json_file:
#     graph_json = json.load(graph_json_file)
# G.set_graph_json(graph_json)

# Adding style to the graph elements
G.add_style('node', {
    "width": "60px",
    "height": "60px",
    "content": "data(id)",
    "pie-size": "80%",
    "pie-1-background-color": "#E8747C",
    "pie-1-background-size": "mapData(foo, 0, 10, 0, 100)",
    "pie-2-background-color": "#74CBE8",
    "pie-2-background-size": "mapData(bar, 0, 10, 0, 100)",
    "pie-3-background-color": "#74E883",
    "pie-3-background-size": "mapData(baz, 0, 10, 0, 100)",
    "background-color": "grey",
    "text-valign": "top"
})
G.add_style('edge', {
    "curve-style": "bezier",
    "width": 4,
    "target-arrow-shape": "triangle",
    "opacity": 0.5,
    "line-color": "grey"
})

# You can also add style by loading the style.json file and setting it for the graph.

# with open('style.json') as style_json_file:
#     style_json = json.load(style_json_file)
# G.set_style_json(style_json)

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
