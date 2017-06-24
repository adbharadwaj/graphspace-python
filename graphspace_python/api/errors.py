class GraphSpaceError(Exception):

    def __init__(self, status_code, reason, response):
        self.status_code = status_code
        self.reason = reason
        self.error_code = response['error_code']
        self.error_message = response['error_message']

    def __str__(self):
        return self.error_message

class BadRequest(GraphSpaceError):
    pass

class UserNotAuthorised(GraphSpaceError):
    pass

class UserNotAuthenticated(GraphSpaceError):
    pass

class IsPublicNotSet(GraphSpaceError):
    pass

class NotAllowedGraphAccess(GraphSpaceError):
    pass

class CannotCreateGraphForOtherUser(GraphSpaceError):
    pass

class NotAllowedGroupAccess(GraphSpaceError):
    pass

class CannotCreateGroupForOtherUser(GraphSpaceError):
    pass

class NotAllowedLayoutAccess(GraphSpaceError):
    pass

class CannotCreateLayoutForOtherUser(GraphSpaceError):
    pass

class LayoutNameAlreadyExists(GraphSpaceError):
    pass

class ErrorHandler(object):

    _error_map = {
        1002: BadRequest,
        1004: UserNotAuthorised,
        1005: UserNotAuthenticated,
        1006: IsPublicNotSet,
        1007: NotAllowedGraphAccess,
        1008: CannotCreateGraphForOtherUser,
        1010: NotAllowedGroupAccess,
        1011: CannotCreateGroupForOtherUser,
        1012: NotAllowedLayoutAccess,
        1013: CannotCreateLayoutForOtherUser,
        1014: LayoutNameAlreadyExists
    }

    def raise_error(self, error, response):
        try:
            raise self._error_map[response['error_code']](
                error.response.status_code,
                error.response.reason,
                response
            )
        except KeyError:
            raise error
