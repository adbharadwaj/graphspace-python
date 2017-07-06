from graphspace_python.api.obj.graph import Graph
from graphspace_python.api.obj.response_object import ResponseObject

class GraphResponse(ResponseObject):
    """GraphResponse Class

    Encapsulates the response from the graphs endpoint.
    """

    _fields = [
        'total'
    ]

    def __init__(self, response):
        """Construct a new 'GraphResponse' object.

        Calls '_parse' method of parent class 'ResponseObject' to parse the response.
        :param response: Response Dict obtained from Graphs API call.
        """
        super(GraphResponse, self).__init__(response)
        self._parse('graph', Graph, response)
