from graphspace_python.api.obj.graph import Graph
from graphspace_python.api.obj.response_object import ResponseObject

class MultipleGraphResponse(ResponseObject):

    _fields = [
        'total'
    ]

    def __init__(self, response):
        super(MultipleGraphResponse, self).__init__(response)
        self._parse('graphs', Graph, response)
