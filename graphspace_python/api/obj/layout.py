from graphspace_python.api.obj.response_object import ResponseObject

class Layout(ResponseObject):

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
        super(Layout, self).__init__(response)
