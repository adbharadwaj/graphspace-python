from graphspace_python.api.obj.graph import Graph
from graphspace_python.api.obj.response_object import ResponseObject

class GraphResponse(ResponseObject):

    _fields = [
        'total',
        'message'
    ]

    def __init__(self, response):
        super(GraphResponse, self).__init__(response)
        self._parse('graph', Graph, response)
