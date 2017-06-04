from graphspace_python.api.obj.graph import Graph
from graphspace_python.api.obj.response_object import ResponseObject

class SingleGraphResponse(ResponseObject):

    def __init__(self, response):
        super(SingleGraphResponse, self).__init__(response)
        self._parse_response_body('graph', Graph, response)
