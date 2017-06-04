from graphspace_python.api.obj.response_object import ResponseObject

class Graph(ResponseObject):

    _fields = [
        'id',
        'name',
        'owner_email',
        'is_public',
        'created_at',
        'updated_at',
        'tags',
        'style_json',
        'graph_json',
        'default_layout_id'
    ]

    def __init__(self, response):
        super(Graph, self).__init__(response)
