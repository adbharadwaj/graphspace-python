from graphspace_python.api.obj.group import Group
from graphspace_python.api.obj.response_object import ResponseObject

class GroupResponse(ResponseObject):
    """GroupResponse Class

    Encapsulates the response from the groups endpoint.
    """

    _fields = [
        'total'
    ]

    def __init__(self, response):
        """Construct a new 'GroupResponse' object.

        Calls '_parse' method of parent class 'ResponseObject' to parse the response.
        :param response: Response Dict obtained from Groups API call.
        """
        super(GroupResponse, self).__init__(response)
        self._parse('group', Group, response)
