from graphspace_python.api.obj.response_object import ResponseObject
from graphspace_python.graphs.classes.gsgroup import GSGroup

class Group(ResponseObject, GSGroup):
    """Group object Class
    Inherits ResponseObject and GSGroup classes.

    Encapsulates details of a group received in response.
    """

    _fields = [
        'id',
        'name',
        'owner_email',
        'description',
        'created_at',
        'updated_at',
        'total_graphs',
        'total_members',
        'invite_code'
    ]

    def __init__(self, response):
        """Construct a new 'Group' object having the attributes specified in '_fields'

        :param response: Dict having group details.
        """
        GSGroup.__init__(self)
        ResponseObject.__init__(self, response)
