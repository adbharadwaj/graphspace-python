import json
from graphspace_python.api.obj.response_object import ResponseObject
from graphspace_python.graphs.classes.gslayout import GSLayout

class Layout(ResponseObject, GSLayout):
    """Layout object Class
    Inherits ResponseObject and GSLayout classes.

    Encapsulates details of a layout received in response.
    """

    _fields = [
        'id',
        'graph_id',
        'name',
        'owner_email',
        'is_shared',
        'created_at',
        'updated_at',
        'style_json',
        'positions_json'
    ]

    def __init__(self, response):
        """Construct a new 'Layout' object having the attributes specified in '_fields'

        :param response: Dict having layout details.
        """
        GSLayout.__init__(self)
        ResponseObject.__init__(self, response)
        self.url = 'http://graphspace.org/graphs/{0}?user_layout={1}'.format(self.graph_id, self.id)
        self._convert_string_to_json()

    def _convert_string_to_json(self):
        """Convert the json dumped string attributes 'positions_json' and 'style_json'
        into Dict type.
        """
        self.style_json = json.loads(self.style_json)
        self.positions_json = json.loads(self.positions_json)
