import pytest
import mock

from graphspace_python.api.client import GraphSpace
from graphspace_python.api.errors import ErrorHandler
error_handler = ErrorHandler()
from graphspace_python.api.errors import GraphSpaceError
from graphspace_python.api.errors import UserNotAuthenticated

def test_error_handling():
    test_error_handler_raises_error_from_api_response()
    test_error_handler_raises_correct_graphspace_error()

def test_error_handler_raises_error_from_api_response():
    graphspace = GraphSpace('user1@example.com', 'user1')
    with pytest.raises(GraphSpaceError) as err:
        graphspace.get_graph(graph_id=3242312)

def test_error_handler_raises_correct_graphspace_error():
    error = mock.Mock()
    error.response.status_code = 401
    error.response.reason = 'Unauthorized'
    response = mock.Mock()
    response = {
        'error_code': 1005,
        'error_message': 'User authentication failed'
    }
    with pytest.raises(UserNotAuthenticated) as err:
        error_handler.raise_error(error, response)

test_error_handling()
