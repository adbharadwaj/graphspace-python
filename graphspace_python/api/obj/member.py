from graphspace_python.api.obj.response_object import ResponseObject

class Member(ResponseObject):
    """Member object Class

    Encapsulates details of a group member received in response.
    """

    _fields = [
        'id',
        'email',
        'created_at',
        'updated_at'
    ]

    def __init__(self, response):
        """Construct a new 'Member' object having the attributes specified in '_fields'

        :param response: Dict having group member details.
        """
        super(Member, self).__init__(response)
