import pytest
from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace
from graphspace_python.api.obj.graph import Graph
from layouts_test import test_layouts_endpoint
from groups_test import test_groups_endpoint
from legend_test import test_gslegend
from graphspace_python.api import errors


def test_graphs_endpoint():
	test_user_not_authenticated_error()
	graph = test_post_graph(name='MyTestGraph')
	test_graph_already_exists_error(name='MyTestGraph')
	test_layouts_endpoint(graph.id)
	test_groups_endpoint(graph.id)
	test_get_graph(name='MyTestGraph')
	test_publish_graph(name='MyTestGraph')
	test_update_graph(name='MyTestGraph')
	test_update_graph2(name='MyTestGraph')
	test_get_public_graphs()
	test_get_shared_graphs()
	test_get_my_graphs()
	test_get_graph_by_id()
	test_delete_graph(name='MyTestGraph')
	test_user_not_authorised_error(graph.id)
	test_gslegend()


def test_graph_already_exists_error(name):
	with pytest.raises(errors.BadRequest) as err:
		test_post_graph(name=name)
		assert err.error_message == "Graph %s already exists for user1@example.com!" % name


def test_user_not_authorised_error(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	with pytest.raises(errors.UserNotAuthorised) as err:
		graphspace.get_graph(graph_id=graph_id)


def test_user_not_authenticated_error():
	graphspace = GraphSpace('user1@example.com', 'WrongPassword')
	with pytest.raises(errors.UserNotAuthenticated) as err:
		graphspace.get_my_graphs()


def test_publish_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graph = graphspace.publish_graph(graph_name=name)
	assert type(graph) is Graph and graph.is_public == 1


def test_update_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')

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

	graph = graphspace.update_graph(graph1)
	assert type(graph) is Graph
	assert graph.get_name() == graph1.get_name() and graph.is_public == 1
	assert len(graph.graph_json['elements']['edges']) == 0
	assert len(graph.graph_json['elements']['nodes']) == 2


def test_update_graph2(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	# Retrieving graph
	graph = graphspace.get_graph(graph_name=name)
	# Modifying the retrieved graph
	graph.set_name(name)
	graph.add_node('z', popup='sample node popup text', label='Z')
	graph.set_is_public()
	# Updating graph
	graph1 = graphspace.update_graph(graph)
	assert type(graph1) is Graph
	assert graph1.get_name() == graph.get_name()
	assert 'z' in graph1.node
	assert graph1.is_public == 1


def test_delete_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.delete_graph(graph_name=name)
	assert graphspace.get_graph(graph_name=name) is None


def test_post_graph(name=None):
	graphspace = GraphSpace('user1@example.com', 'user1')
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
	graph = graphspace.post_graph(graph1)
	assert type(graph) is Graph
	assert graph.get_name() == graph1.get_name()
	return graph


def test_get_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graph = graphspace.get_graph(graph_name=name)
	assert type(graph) is Graph
	assert graph.get_name() == name


def test_get_graph_by_id():
	graphspace = GraphSpace('flud', 'Muraliistheman!')
	# graphspace.set_api_host('localhost:8000')
	graph = graphspace.get_graph(graph_id=20047)
	assert type(graph) is Graph
	assert graph.id == 20047


def test_get_public_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphs = graphspace.get_public_graphs(tags=['Kegg-networks'])
	assert all(isinstance(x, Graph) for x in graphs)
	assert len(graphs) >= 0


def test_get_shared_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	# response = graphspace.get_public_graphs(tags=['2015-bioinformatics-xtalk', 'kegg-curated-top-rank-FPs'])
	graphs = graphspace.get_shared_graphs()
	assert all(isinstance(x, Graph) for x in graphs)
	assert len(graphs) >= 0


def test_get_my_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	# response = graphspace.get_public_graphs(tags=['2015-bioinformatics-xtalk', 'kegg-curated-top-rank-FPs'])
	graphs = graphspace.get_my_graphs()
	assert all(isinstance(x, Graph) for x in graphs)
	assert len(graphs) > 0


test_graphs_endpoint()
