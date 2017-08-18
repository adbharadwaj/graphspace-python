import json
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Initialize graph
G = GSGraph()
# Set name, tags and visibility status
G.set_name('Visual Style')
G.set_tags(['visual'])
G.set_is_public()
# Define and set data
data = {
    'description': 'A demo visual network.<br>You can also view this demo graph at:\
 <a href=\"http://js.cytoscape.org/demos/visual-style/\">http://js.cytoscape.org/demos/visual-style/</a>',
    'directed': True
}
G.set_data(data)

# Construct nodes and edges of the graph
# Add nodes
G.add_node('j', {"weight": 65, "faveColor": "#6FB1FC"}, label='Jerry')
G.add_node('e', {"weight": 45, "faveColor": "#EDA1ED"}, label='Elaine')
G.add_node('k', {"weight": 75, "faveColor": "#86B342"}, label='Kramer')
G.add_node('g', {"weight": 70, "faveColor": "#F5A45D"}, label='George')
# Set node positions
G.set_node_position('j', y=482.1, x=529.9)
G.set_node_position('e', y=482.4, x=641.8)
G.set_node_position('k', y=606.4, x=577.3)
G.set_node_position('g', y=597.5, x=456.4)
# Add edges
G.add_edge('j', 'e', {"faveColor": "#6FB1FC", "strength": 90})
G.add_edge('j', 'k', {"faveColor": "#6FB1FC", "strength": 70})
G.add_edge('j', 'g', {"faveColor": "#6FB1FC", "strength": 80})
G.add_edge('e', 'j', {"faveColor": "#EDA1ED", "strength": 95})
G.add_edge('e', 'k', {"faveColor": "#EDA1ED", "strength": 60, "type": "questionable"})
G.add_edge('k', 'j', {"faveColor": "#86B342", "strength": 100})
G.add_edge('k', 'e', {"faveColor": "#86B342", "strength": 100})
G.add_edge('k', 'g', {"faveColor": "#86B342", "strength": 100})
G.add_edge('g', 'j', {"faveColor": "#F5A45D", "strength": 90})

# You can also construct the nodes and edges of the graph by loading the graph.json
# file and setting it for the graph.

# with open('graph.json') as graph_json_file:
#     graph_json = json.load(graph_json_file)
# G.set_graph_json(graph_json)

# Adding style to the graph elements
G.add_style('node', {
    "width": "mapData(weight, 40, 80, 20, 60)",
    "content": "data(label)",
    "text-valign": "center",
    "text-outline-width": 2,
    "text-outline-color": "data(faveColor)",
    "background-color": "data(faveColor)",
    "color": "#fff"
})
G.add_style('node[name="j"]', {
    "shape": "triangle"
})
G.add_style('node[name="e"]', {
    "shape": "ellipse"
})
G.add_style('node[name="k"]', {
    "shape": "octagon"
})
G.add_style('node[name="g"]', {
    "shape": "rectangle"
})
G.add_style('edge', {
    "curve-style": "bezier",
    "opacity": 0.666,
    "width": "mapData(strength, 70, 100, 2, 6)",
    "target-arrow-shape": "triangle",
    "source-arrow-shape": "circle",
    "line-color": "data(faveColor)",
    "source-arrow-color": "data(faveColor)",
    "target-arrow-color": "data(faveColor)"
})
G.add_style('edge[type = "questionable"]', {
    "line-style": "dotted",
    "target-arrow-shape": "diamond"
})

# You can also add style by loading the style.json file and setting it for the graph.

# with open('style.json') as style_json_file:
#     style_json = json.load(style_json_file)
# G.set_style_json(style_json)

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
