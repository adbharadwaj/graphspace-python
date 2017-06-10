from graphspace_python.api.obj.layout import Layout
from graphspace_python.api.obj.response_object import ResponseObject

class LayoutResponse(ResponseObject):

    _fields = [
        'total',
        'message'
    ]

    def __init__(self, response):
        super(LayoutResponse, self).__init__(response)
        self._parse('layout', Layout, response)
