import json
from graphspace_python.api.obj.response_object import ResponseObject
from graphspace_python.graphs.classes.gslayout import GSLayout

class Layout(ResponseObject, GSLayout):

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
        GSLayout.__init__(self)
        ResponseObject.__init__(self, response)
        self._convert_string_to_json()

    def _convert_string_to_json(self):
        # Convert the positions_json and style_json strings in the response to json dict
        self.style_json = json.loads(self.style_json)
        self.positions_json = json.loads(self.positions_json)
