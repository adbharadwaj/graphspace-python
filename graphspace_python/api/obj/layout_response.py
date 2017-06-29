from graphspace_python.api.obj.layout import Layout
from graphspace_python.api.obj.response_object import ResponseObject

class LayoutResponse(ResponseObject):
    """LayoutResponse Class

    Encapsulates the response from the layouts endpoint.
    """

    _fields = [
        'total'
    ]

    def __init__(self, response):
        """Construct a new 'LayoutResponse' object

        Calls '_parse' method of parent class 'ResponseObject' to parse the response.
        :param response: Response Dict obtained from Layouts API call.
        """
        super(LayoutResponse, self).__init__(response)
        self._parse('layout', Layout, response)
