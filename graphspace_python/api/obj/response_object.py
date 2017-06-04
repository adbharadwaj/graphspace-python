class ResponseObject(object):
    _fields = []

    def __init__(self, response):
        for field in self._fields:
            value = response[field] if field in response else None
            self.__setattr__(field, value)

    def _parse(self, field_name, cls_name, response):
        if response and field_name in response:
            self.__setattr__(
                field_name,
                [cls_name(field) for field in response[field_name]]
            )

    def _parse_response_body(self, field_name, cls_name, response):
        self.__setattr__(field_name, cls_name(response))
