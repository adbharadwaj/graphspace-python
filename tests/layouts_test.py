from graphspace_python.api.client import GraphSpace
from graphspace_python.api.obj.layout_response import LayoutResponse


def test_layouts_endpoint():
	layout = test_post_graph_layout(graph_id=graph['id'])
	test_get_my_graph_layouts(graph_id=graph['id'])
	test_update_graph_layout(graph_id=graph['id'], layout_id=layout['id'])
	test_get_shared_graph_layouts(graph_id=graph['id'])
	test_delete_graph_layout(graph_id=graph['id'], layout_id=layout['id'])


def test_get_my_graph_layouts(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_my_graph_layouts(graph_id=graph_id)
	assert hasattr(response, 'layouts') and len(response.layouts) >= 0


def test_get_shared_graph_layouts(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_shared_graph_layouts(graph_id=graph_id)
	assert hasattr(response, 'layouts') and len(response.layouts) >= 0


def test_post_graph_layout(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.post_graph_layout(graph_id=graph_id, layout_name='test layout')
	assert hasattr(response, 'layout') and response.layout.is_shared == 0
	return response


def test_update_graph_layout(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.update_graph_layout(graph_id=graph_id, layout_id=layout_id, layout_name='updated test layout', is_shared=1)
	assert hasattr(response, 'layout') and response.layout.is_shared == 1 and response.layout.name == 'updated test layout'


def test_delete_graph_layout(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	graphspace.delete_graph_layout(graph_id=graph_id, layout_id=layout_id)
	assert graphspace.get_graph_layout(graph_id=graph_id, layout_id=layout_id) is None
