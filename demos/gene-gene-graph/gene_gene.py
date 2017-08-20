import urllib
import json
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Fetch the graph data
data_url = 'https://raw.githubusercontent.com/cytoscape/cytoscape.js/master/documentation/demos/colajs-graph/data.json'
response = urllib.urlopen(data_url)
graph_data = json.loads(response.read())

# Fetch the style data
data_url = 'https://raw.githubusercontent.com/cytoscape/cytoscape.js/master/documentation/demos/colajs-graph/cy-style.json'
response = urllib.urlopen(data_url)
style_data = json.loads(response.read())

# Initialize graph
G = GSGraph()
# Set name, tags and visibility status
G.set_name('Gene-gene graph')
G.set_tags(['gene-gene', 'graphspace', 'demo'])
G.set_is_public()
# Define and set data
data = {
    'description': 'This is a demo of a graph of gene-gene interactions.<br>View functional demo of this graph at:\
 <a href=\"http://js.cytoscape.org/demos/colajs-graph/\">http://js.cytoscape.org/demos/colajs-graph/</a>',
    'directed': False
}
G.set_data(data)

# Construct nodes and edges of the graph from graph data
for elem in graph_data:
    if elem['group'] == 'nodes':
        popup = ("<a target=\"_blank\" href=\"http://www.genecards.org/cgi-bin/carddisp.pl?gene=" + elem['data']['name']
                + "\">GeneCard</a><br><a target=\"_blank\" href=\"http://www.uniprot.org/uniprot/?query=" + elem['data']['name']
                + "&fil=organism%3A%22Homo+sapiens+%28Human%29+%5B9606%5D%22&sort=score\">UniProt search</a><br><a target=\"_blank\" href=\"http://genemania.org/search/human/"
                + elem['data']['name'] + "\">GeneMANIA</a>")
        G.add_node(elem['data']['id'], elem['data'], elem['data']['name'], popup)
        G.set_node_position(elem['data']['id'], elem['position']['y'], elem['position']['x'])
    else:
        G.add_edge(elem['data']['source'], elem['data']['target'], elem['data'])

# Set style_json for the graph
del style_data[1]['style']['content']
style_json = {
    'style': style_data
}
G.set_style_json(style_json)

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
