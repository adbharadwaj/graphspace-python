from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace

# Initialize client with your username and password
graphspace = GraphSpace('user1@example.com', 'user1')

# Initialize graph
G = GSGraph()
# Set name, tags and visibility status
G.set_name('Popup Demo')
G.set_tags(['popup', 'graphspace', 'demo'])
G.set_is_public()
# Define and set data
data = {
    'description': 'This is a demo graph showing functionality of popup in GraphSpace.'
}
G.set_data(data)

# Add node to the graph
G.add_node('n', label='Tap me!', popup='Hello!')
# Define node style
G.add_style('node', {
    "content": "data(label)",
    "background-color": "grey",
    "text-valign": "top"
})

# Post graph to GraphSpace
graph = graphspace.post_graph(G)
print('Your graph has been saved on GraphSpace. You can view it at %s.' % graph.url)
