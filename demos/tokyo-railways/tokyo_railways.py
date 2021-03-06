import urllib
import json
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Fetch the graph data
data_url = 'https://cdn.rawgit.com/maxkfranz/934042c1ecc464a8de85/raw'
response = urllib.urlopen(data_url)
graph_data = json.loads(response.read())

# Load the style json file
with open('style.json') as style_json_file:
    style_json = json.load(style_json_file)

# Initialize graph
G = GSGraph()
# Set name, tags and visibility status
G.set_name('Tokyo Railways')
G.set_tags(['tokyo-railways', 'graphspace', 'demo'])
G.set_is_public()
# Define and set data
data = {
    'description': 'Graphical representation of railway network of Tokyo.<br>View functional demo of this graph at:\
 <a href=\"http://js.cytoscape.org/demos/tokyo-railways/\">http://js.cytoscape.org/demos/tokyo-railways/</a>',
    'directed': False
}
G.set_data(data)

# Construct nodes and edges of the graph from graph data
for node in graph_data['elements']['nodes']:
    G.add_node(node['data']['id'], node['data'])
    G.set_node_position(node['data']['id'], node['position']['y'], node['position']['x'])
for edge in graph_data['elements']['edges']:
    G.add_edge(edge['data']['source'], edge['data']['target'], edge['data'])

# Set style_json for the graph
G.set_style_json(style_json)

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
