class GraphSpaceError(Exception):
    """GraphSpaceError class

    Base error class for the GraphSpace HTTPErrors.
    """

    def __init__(self, status_code, reason, response):
        """Construct a new 'GraphSpaceError' object.

        :param status_code: Status Code of the HTTPError.
        :param reason: Reason of HTTPError.
        :response: Response dict having error details from the API call.
        """
        self.status_code = status_code
        self.reason = reason
        self.error_code = response['error_code']
        self.error_message = response['error_message']

    def __str__(self):
        """Prints the error message when exception occurs.
        """
        return self.error_message

class BadRequest(GraphSpaceError):
    pass

class UserNotAuthorised(GraphSpaceError):
    pass

class UserNotAuthenticated(GraphSpaceError):
    pass

class LayoutNameAlreadyExists(GraphSpaceError):
    pass

class ErrorHandler(object):
    """ErrorHandler class

    Exception handling class for GraphSpace API's HTTPErrors.
    """

    _error_map = {
        1002: BadRequest,
        1004: UserNotAuthorised,
        1005: UserNotAuthenticated,
        1014: LayoutNameAlreadyExists
    }

    def raise_error(self, error, response):
        """Raises exception based on the error code when any HTTPError occurs in API call.

        :param error: HTTPError object.
        :param response: Response dict having error details from the API call.
        """
        try:
            raise self._error_map[response['error_code']](
                error.response.status_code,
                error.response.reason,
                response
            )
        except KeyError:
            raise error
