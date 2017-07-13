class ResponseObject(object):
    """ResponseObject Class
    """

    _fields = []

    def __init__(self, response):
        """Construct a new 'ResponseObject' object.

        Creates certain attributes of the object and assigns them value
        if that attribute is present in response Dict.

        :param response: Response Dict obtained from API call.
        """
        for field in self._fields:
            value = response[field] if field in response else None
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
            # depict that the response has multiple entities else single entity
            if 'total' in response:
                field_name += 's'
                # Set an attribute by the plural of field_name (multiple entities) and
                # assign it an array of objects of the class passed as param cls_name
                self.__setattr__(
                    field_name,
                    [cls_name(field) for field in response[field_name]]
                )
            else:
                # Set an attribute by the field_name and assign an object of the class type
                # (cls_name) to the attribute.
                self.__setattr__(field_name, cls_name(response))
