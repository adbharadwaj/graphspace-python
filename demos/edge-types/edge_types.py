import json
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Load the graph json file
with open('graph.json') as graph_json_file:
    graph_json = json.load(graph_json_file)

# Load the style json file
with open('style.json') as style_json_file:
    style_json = json.load(style_json_file)

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

# Set graph_json and style_json
G.set_graph_json(graph_json)
G.set_style_json(style_json)

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
