from graphspace_python.api.obj.response_object import ResponseObject
from graphspace_python.graphs.classes.gsgraph import GSGraph

class Graph(ResponseObject, GSGraph):

    _fields = [
        'id',
        'name',
        'owner_email',
        'is_public',
        'created_at',
        'updated_at',
        'tags',
        'style_json',
        'graph_json',
        'default_layout_id'
    ]

    def __init__(self, response):
        GSGraph.__init__(self)
        ResponseObject.__init__(self, response)
        self.set_data(self.graph_json['data'])
        self._assign_nodes_and_edges()

    def _assign_nodes_and_edges(self):
        # Add the nodes and edges of the fetched graph to the GSGraph class' nodes and edges
        # This will ensure that the nodes and edges of the fetched graph are not lost when 
        # compute_graph_json() is called.
        nodes = self.graph_json['elements']['nodes']
        for node in nodes:
            self.add_node(node['data']['id'], node)
        edges = self.graph_json['elements']['edges']
        for edge in edges:
            self.add_edge(edge['data']['source'], edge['data']['target'], edge)
