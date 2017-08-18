import json
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Initialize graph
G = GSGraph()
# Set name, tags and visibility status
G.set_name('Edge Types Demo')
G.set_tags(['edge-types'])
G.set_is_public()
# Define and set data
data = {
    'description': 'This is a demo graph showing different types of edges. You can also view this demo graph at:\
 <a href=\"http://js.cytoscape.org/demos/edge-types/\">http://js.cytoscape.org/demos/edge-types/</a>',
    'directed': False
}
G.set_data(data)

# Construct nodes and edges of the graph
# Add nodes
G.add_node('n01', label='bezier')
G.add_node('n02')
G.add_node('n03', label='unbundled-bezier')
G.add_node('n04')
G.add_node('n05', label='unbundled-bezier(multiple)')
G.add_node('n06')
G.add_node('n07', label='haystack')
G.add_node('n08')
G.add_node('n09', label='segments')
G.add_node('n10')
# Set node positions
G.set_node_position('n01', y=142.4, x=108.1)
G.set_node_position('n02', y=142.4, x=391.8)
G.set_node_position('n03', y=142.2, x=670.1)
G.set_node_position('n04', y=146.6, x=966.1)
G.set_node_position('n05', y=342.9, x=110.7)
G.set_node_position('n06', y=340.2, x=385.2)
G.set_node_position('n07', y=343.3, x=666.2)
G.set_node_position('n08', y=344.9, x=969.5)
G.set_node_position('n09', y=540.4, x=104.4)
G.set_node_position('n10', y=539.2, x=397.6)
# Add edges
G.add_edge('n09', 'n10', {'type': 'segments'})
G.add_edge('n08', 'n07', {'type': 'haystack'})
G.add_edge('n05', 'n06', {'type': 'multi-unbundled-bezier'})
G.add_edge('n01', 'n02', {'type': 'bezier'})
G.add_edge('n03', 'n04', {'type': 'unbundled-bezier'})
G.add_edge('n02', 'n01', {'type': 'bezier'})

# You can also construct the nodes and edges of the graph by loading the graph.json
# file and setting it for the graph.

# with open('graph.json') as graph_json_file:
#     graph_json = json.load(graph_json_file)
# G.set_graph_json(graph_json)

# Adding style to the graph elements
G.add_style('node', {
    "height": 40,
    "width": 40,
    "background-color": "#333",
    "text-valign": "center",
    "text-halign": "left"
})
G.add_style('edge', {
    "width": 3,
    "opacity": 0.666,
    "line-color": "#888"
})
G.add_style('edge[type="bezier"]', {
    "curve-style": "bezier",
    "control-point-step-size": 40
})
G.add_style('edge[type="unbundled-bezier"]', {
    "curve-style": "unbundled-bezier",
    "control-point-distances": 120,
    "control-point-weights": 0.1
})
G.add_style('edge[type="multi-unbundled-bezier"]', {
    "curve-style": "unbundled-bezier",
    "control-point-distances": [40, -40],
    "control-point-weights": [0.250, 0.75]
})
G.add_style('edge[type="haystack"]', {
    "curve-style": "haystack",
    "haystack-radius": 0.5
})
G.add_style('edge[type="segments"]', {
    "curve-style": "segments",
    "segment-distances": [ 40, -40 ],
    "segment-weights": [0.250 , 0.75]
})

# You can also add style by loading the style.json file and setting it for the graph.

# with open('style.json') as style_json_file:
#     style_json = json.load(style_json_file)
# G.set_style_json(style_json)

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
