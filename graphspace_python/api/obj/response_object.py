class ResponseObject(object):
    _fields = []

    def __init__(self, response):
        for field in self._fields:
            if field in response:
                value = response[field]
                self.__setattr__(field, value)

    def _parse(self, field_name, cls_name, response):
        if response:
            if 'total' in response:
                field_name += 's'
                self.__setattr__(
                    field_name,
                    [cls_name(field) for field in response[field_name]]
                )
            elif 'message' not in response:
                self.__setattr__(field_name, cls_name(response))
