class ResponseObject(object):
    _fields = []

    def __init__(self, response):
        for field in self._fields:
            value = response[field] if field in response else None
            self.__setattr__(field, value)

    def _parse(self, field_name, cls_name, response):
        if response and 'total' in response:
            field_name += 's'
            self.__setattr__(
                field_name,
                [cls_name(field) for field in response[field_name]]
            )
        else:
            self.__setattr__(field_name, cls_name(response))
