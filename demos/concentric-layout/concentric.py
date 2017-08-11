import urllib
import json
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Fetch the graph data
data_url = 'https://raw.githubusercontent.com/cytoscape/cytoscape.js/master/documentation/demos/concentric-layout/data.json'
response = urllib.urlopen(data_url)
graph_data = json.loads(response.read())

# Initialize graph
G = GSGraph()
# Set name, tags and visibility status
G.set_name('Concentric Layout')
G.set_tags(['concentric-layout'])
G.set_is_public()
# Define and set data
data = {
    'description': 'This is a demo graph having concentric layout. You can also view this demo graph at:\
 <a href=\"http://js.cytoscape.org/demos/concentric-layout/\">http://js.cytoscape.org/demos/concentric-layout/</a>',
    'directed': True
}
G.set_data(data)

# Construct nodes and edges of the graph from graph data
for elem in graph_data:
    if elem['group'] == 'nodes':
        G.add_node(elem['data']['id'], elem['data'])
        G.set_node_position(elem['data']['id'], elem['position']['y'], elem['position']['x'])
    else:
        G.add_edge(elem['data']['source'], elem['data']['target'], elem['data'])

# Define style for the graph
style_json = {
    "style": [
        {
            'selector': 'node',
            'style': {
                'height': 20,
                'width': 20,
                'background-color': '#30c9bc'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'haystack',
                'haystack-radius': 0,
                'width': 5,
                'opacity': 0.5,
                'line-color': '#a8eae5'
            }
        }
    ]
}
G.set_style_json(style_json)

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
