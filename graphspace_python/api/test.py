from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace


def test_graph_crud():
	test_post_graph(name='MyTestGraph')
	test_get_graph(name='MyTestGraph')
	test_make_graph_public(name='MyTestGraph')
	test_update_graph(name='MyTestGraph')
	test_delete_graph(name='MyTestGraph')
	test_get_public_graphs()


def test_make_graph_public(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	assert graphspace.make_graph_public(name)['is_public'] == 1


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

	graph1.set_data(data={
		'description': 'my sample graph'
	})
	response = graphspace.update_graph(name, graph=graph1, is_public=1)
	assert 'name' in response and response['name'] == graph1.get_name()
	assert response['is_public'] == 1
	assert len(response['graph_json']['elements']['edges']) == 0
	assert len(response['graph_json']['elements']['nodes']) == 2


def test_delete_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	graphspace.delete_graph(name)
	assert graphspace.get_graph(name) is None


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
	assert 'name' in response and response['name'] == graph1.get_name()


def test_get_graph(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	graph = graphspace.get_graph(name)
	assert graph is not None and graph['name'] == name


def test_get_public_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_public_graphs(tags=['Kegg-networks'])
	assert response is not None and len(response['graphs']) > 0


def test_get_shared_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	# response = graphspace.get_public_graphs(tags=['2015-bioinformatics-xtalk', 'kegg-curated-top-rank-FPs'])
	response = graphspace.get_shared_graphs()
	assert response is not None and len(response['graphs']) > 0


def test_get_my_graphs():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	# response = graphspace.get_public_graphs(tags=['2015-bioinformatics-xtalk', 'kegg-curated-top-rank-FPs'])
	response = graphspace.get_my_graphs()
	assert response is not None and len(response['graphs']) > 0

# test_get_public_graphs()
# test_graph_crud()