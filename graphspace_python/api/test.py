from graphspace_python.graphs.classes.gsgraph import GSGraph
from graphspace_python.api.client import GraphSpace


def test_graphspace_python():
	test_post_graph(name='MyTestGraph')
	graph = test_get_graph(name='MyTestGraph')
	test_make_graph_public(name='MyTestGraph')
	test_update_graph(name='MyTestGraph')
	test_update_graph2(name='MyTestGraph')
	test_get_public_graphs()
	test_get_shared_graphs()
	test_get_my_graphs()
	layout = test_post_graph_layout(graph_id=graph['id'])
	test_get_my_graph_layouts(graph_id=graph['id'])
	test_update_graph_layout(graph_id=graph['id'], layout_id=layout['id'])
	test_get_shared_graph_layouts(graph_id=graph['id'])
	test_delete_graph_layout(graph_id=graph['id'], layout_id=layout['id'])
	test_delete_graph(name='MyTestGraph')


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


def test_update_graph2(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	# Retrieving graph
	graph = graphspace.get_graph(name)
	# Creating updated graph object
	G = GSGraph()
	G.set_graph_json(graph.get('graph_json'))
	G.set_style_json(graph.get('style_json'))
	G.set_name(graph.get('name'))
	G.set_tags(graph.get('name'))
	# Updating graph
	response = graphspace.update_graph(name, graph=G, is_public=1)
	assert 'name' in response and response['name'] == G.get_name()
	assert response['is_public'] == 1


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
	return graph


def test_get_graph_by_id():
	graphspace = GraphSpace('flud', 'Muraliistheman!')
	# graphspace.set_api_host('localhost:8000')
	graph = graphspace.get_graph_by_id(20047)
	assert graph is not None and 'id' in graph


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


def test_get_my_graph_layouts(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_my_graph_layouts(graph_id=graph_id)
	assert response is not None and len(response['layouts']) >= 0


def test_get_shared_graph_layouts(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_shared_graph_layouts(graph_id=graph_id)
	assert response is not None and len(response['layouts']) >= 0


def test_post_graph_layout(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.post_graph_layout(graph_id=graph_id, layout_name='test layout')
	assert response is not None and response['is_shared'] == 0
	return response


def test_update_graph_layout(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.update_graph_layout(graph_id=graph_id, layout_id=layout_id, layout_name='updated test layout', is_shared=1)
	assert response is not None and response['is_shared'] == 1 and response['name'] == 'updated test layout'


def test_delete_graph_layout(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	graphspace.delete_graph_layout(graph_id=graph_id, layout_id=layout_id)
	assert graphspace.get_graph_layout(graph_id=graph_id, layout_id=layout_id) is None

# test_get_graph_by_id()
# test_graphspace_python()
# test_post_graph(name='MyTestGraph')
# test_delete_graph(name='MyTestGraph')