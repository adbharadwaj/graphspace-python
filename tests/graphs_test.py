import pytest
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace
from graphspace_python.api.obj.api_response import APIResponse
from layouts_test import test_layouts_endpoint
from groups_test import test_groups_endpoint
from graphspace_python.api import errors


def test_graphs_endpoint():
	test_user_not_authenticated_error()
	graph = test_post_graph(name='MyTestGraph')
	test_graph_already_exists_error(name='MyTestGraph')
	test_layouts_endpoint(graph.id)
	test_groups_endpoint(graph.id)
	test_get_graph(name='MyTestGraph')
	test_make_graph_public(name='MyTestGraph')
	test_update_graph(name='MyTestGraph')
	test_update_graph2(name='MyTestGraph')
	test_get_public_graphs()
	test_get_shared_graphs()
	test_get_my_graphs()
	test_get_graph_by_id()
	test_delete_graph(name='MyTestGraph')
	test_user_not_authorised_error(graph.id)


def test_graph_already_exists_error(name):
	with pytest.raises(errors.BadRequest) as err:
		test_post_graph(name=name)
		assert err.error_message == "Graph %s already exists for user1@example.com!" % name


def test_user_not_authorised_error(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	with pytest.raises(errors.UserNotAuthorised) as err:
		graphspace.get_graph(graph_id=graph_id)


def test_user_not_authenticated_error():
	graphspace = GraphSpace('user1@example.com', 'WrongPassword')
	graphspace.set_api_host('localhost:8000')
	with pytest.raises(errors.UserNotAuthenticated) as err:
		graphspace.get_my_graphs()


def test_make_graph_public(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.make_graph_public(name=name)
	assert type(response) is APIResponse and response.graph.is_public == 1


def test_update_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')

	graph1 = GSGraph()
	if name is not None:
		graph1.set_name(name)
	graph1.add_node('a', popup='sample node popup text', label='A updated')
	graph1.add_node_style('a', shape='ellipse', color='green', width=90, height=90)
	graph1.add_node('b', popup='sample node popup text', label='B updated')
	graph1.add_node_style('b', shape='ellipse', color='yellow', width=40, height=40)
	graph1.set_is_public()
	graph1.set_data(data={
		'description': 'my sample graph'
	})

	response = graphspace.update_graph(graph=graph1, name=name)
	assert type(response) is APIResponse
	assert hasattr(response, 'graph') and response.graph.name == graph1.get_name()
	assert response.graph.is_public == 1
	assert len(response.graph.graph_json['elements']['edges']) == 0
	assert len(response.graph.graph_json['elements']['nodes']) == 2


def test_update_graph2(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	# Retrieving graph
	graph = graphspace.get_graph(name=name).graph
	# Modifying the retrieved graph
	graph.set_name(name)
	graph.add_node('z', popup='sample node popup text', label='Z')
	graph.set_is_public()
	# Updating graph
	response = graphspace.update_graph(graph=graph, name=name)
	assert type(response) is APIResponse
	assert hasattr(response, 'graph') and response.graph.name == graph.get_name()
	assert 'z' in response.graph.node.keys()
	assert response.graph.is_public == 1


def test_delete_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	graphspace.delete_graph(name=name)
	assert graphspace.get_graph(name=name) is None


def test_post_graph(name=None):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	graph1 = GSGraph()
	if name is not None:
		graph1.set_name(name)
	graph1.add_node('a', popup='sample node popup text', label='A')
	graph1.add_node_style('a', shape='ellipse', color='red', width=90, height=90)
	graph1.add_node('b', popup='sample node popup text', label='B')
	graph1.add_node_style('b', shape='ellipse', color='blue', width=40, height=40)

	graph1.add_edge('a', 'b', directed=True, popup='sample edge popup')
	graph1.add_edge_style('a', 'b', directed=True, edge_style='dotted')
	graph1.set_data(data={
		'description': 'my sample graph'
	})
	graph1.set_tags(['sample'])
	response = graphspace.post_graph(graph1)
	assert type(response) is APIResponse
	assert hasattr(response, 'graph') and response.graph.name == graph1.get_name()
	return response.graph


def test_get_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_graph(name=name)
	assert type(response) is APIResponse
	assert hasattr(response, 'graph') and response.graph.name == name


def test_get_graph_by_id():
	graphspace = GraphSpace('flud', 'Muraliistheman!')
	# graphspace.set_api_host('localhost:8000')
	response = graphspace.get_graph(graph_id=20047)
	assert type(response) is APIResponse
	assert hasattr(response, 'graph') and response.graph.id == 20047


def test_get_public_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_public_graphs(tags=['Kegg-networks'])
	assert type(response) is APIResponse
	assert hasattr(response, 'graphs') and len(response.graphs) > 0


def test_get_shared_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	# response = graphspace.get_public_graphs(tags=['2015-bioinformatics-xtalk', 'kegg-curated-top-rank-FPs'])
	response = graphspace.get_shared_graphs()
	assert type(response) is APIResponse
	assert hasattr(response, 'graphs') and len(response.graphs) > 0


def test_get_my_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	# response = graphspace.get_public_graphs(tags=['2015-bioinformatics-xtalk', 'kegg-curated-top-rank-FPs'])
	response = graphspace.get_my_graphs()
	assert type(response) is APIResponse
	assert hasattr(response, 'graphs') and len(response.graphs) > 0
