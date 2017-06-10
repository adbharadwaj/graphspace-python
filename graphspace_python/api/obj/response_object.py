class ResponseObject(object):
    _fields = []

    def __init__(self, response):
        """Creates certain attributes of the class object and assigns them value
        if that attribute is present in response Dict.

        :param response: Response Dict obtained from API call.
        """
        for field in self._fields:
            if field in response:
                value = response[field]
                self.__setattr__(field, value)

    def _parse(self, field_name, cls_name, response):
        """Parses the response from API call and produces the desired object.

        :param field_name: Name of field (string) to be created as an attribute
         in the class object.
        :param cls_name: Class whose object is to be created and assigned to the
         attribute with the field name.
        :param response: Response Dict obtained from API call.
        """
        if response:
            # Check if there is a 'total' field in the response which will
            # depict that the response is a multiple entity Dict
            if 'total' in response:
                field_name += 's'
                # Set a attribute by the plural of field_name (multiple entities)
                # and assign an array of objects of the class type (passed as param cls_name)
                # to the attribute.
                self.__setattr__(
                    field_name,
                    [cls_name(field) for field in response[field_name]]
                )
            # If there is no 'total' and 'message' field in the response then its
            # a single entity response Dict
            elif 'message' not in response:
                # Set a attribute by the field_name and assign an object of the class type
                # (cls_name) to the attribute.
                self.__setattr__(field_name, cls_name(response))
