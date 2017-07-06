from graphspace_python.api.obj.member import Member
from graphspace_python.api.obj.response_object import ResponseObject

class MemberResponse(ResponseObject):
    """MemberResponse Class

    Encapsulates the response from the group members endpoint.
    """

    _fields = [
        'total'
    ]

    def __init__(self, response):
        """Construct a new 'MemberResponse' object.

        Calls '_parse' method of parent class 'ResponseObject' to parse the response.
        :param response: Response Dict obtained from Group members API call.
        """
        super(MemberResponse, self).__init__(response)
        self._parse('member', Member, response)
