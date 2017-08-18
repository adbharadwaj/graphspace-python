import json
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Initialize graph
G = GSGraph()
# Set name, tags and visibility status
G.set_name('Compound Nodes')
G.set_tags(['compound-nodes'])
G.set_is_public()
# Define and set data
data = {
    'description': 'This is a demo graph having compund nodes. You can also view this demo graph at:\
 <a href=\"http://js.cytoscape.org/demos/compound-nodes/\">http://js.cytoscape.org/demos/compound-nodes/</a>',
    'directed': True
}
G.set_data(data)

# Construct nodes and edges of the graph
# Add nodes
G.add_node('a', parent='b')
G.add_node('b')
G.add_node('c', parent='b')
G.add_node('d')
G.add_node('e')
G.add_node('f', parent='e')
# Set node positions
G.set_node_position('a', x=215, y=85)
G.set_node_position('c', x=300, y=85)
G.set_node_position('d', x=215, y=175)
G.set_node_position('f', x=300, y=175)
# Add edges
G.add_edge('a', 'd')
G.add_edge('e', 'b')

# You can also construct the nodes and edges of the graph by loading the graph.json
# file and setting it for the graph.

# with open('graph.json') as graph_json_file:
#     graph_json = json.load(graph_json_file)
# G.set_graph_json(graph_json)

# Adding style to the graph elements
G.add_style('node', {
    "content": "data(id)",
    "text-valign": "center",
    "text-halign": "center",
    "background-color": "grey"
})
G.add_style('$node > node', {
    "padding-top": "10px",
    "padding-left": "10px",
    "padding-bottom": "10px",
    "padding-right": "10px",
    "text-valign": "top",
    "text-halign": "center",
    "background-color": "#bbb"
})
G.add_style('edge', {
    "target-arrow-shape": "triangle",
    "line-color": "grey"
})

# You can also add style by loading the style.json file and setting it for the graph.

# with open('style.json') as style_json_file:
#     style_json = json.load(style_json_file)
# G.set_style_json(style_json)

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
