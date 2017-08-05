import pytest
from graphspace_python.graphs.classes.gslayout import GSLayout
from graphspace_python.api.client import GraphSpace
from graphspace_python.api.obj.layout import Layout
from graphspace_python.api import errors


def test_layouts_endpoint(graph_id):
	layout = test_post_graph_layout(graph_id=graph_id, name='MyTestLayout')
	test_layout_name_already_exists_error(graph_id=graph_id, name='MyTestLayout')
	test_set_default_graph_layout(layout)
	test_unset_default_graph_layout(graph_id)
	test_get_graph_layout(graph_id=graph_id, name='MyTestLayout')
	test_update_graph_layout(graph_id=graph_id, layout_id=layout.id)
	test_update_graph_layout2(graph_id=graph_id, name='MyTestLayout')
	test_get_my_graph_layouts(graph_id=graph_id)
	test_get_shared_graph_layouts(graph_id=graph_id)
	test_delete_graph_layout(graph_id=graph_id, name='MyTestLayout')
	test_user_not_authorised_error(graph_id=graph_id, layout_id=layout.id)


def test_user_not_authorised_error(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	with pytest.raises(errors.UserNotAuthorised) as err:
		graphspace.get_graph_layout(graph_id=graph_id, layout_id=layout_id)


def test_layout_name_already_exists_error(graph_id, name):
	with pytest.raises(errors.LayoutNameAlreadyExists) as err:
		test_post_graph_layout(graph_id=graph_id, name=name)


def test_set_default_graph_layout(layout):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graph = graphspace.set_default_graph_layout(layout=layout)
	assert graph.default_layout_id == layout.id


def test_unset_default_graph_layout(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graph = graphspace.unset_default_graph_layout(graph_id=graph_id)
	assert graph.default_layout_id is None


def test_get_my_graph_layouts(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	layouts = graphspace.get_my_graph_layouts(graph_id=graph_id)
	assert all(isinstance(x, Layout) for x in layouts)
	assert len(layouts) >= 0


def test_get_shared_graph_layouts(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	layouts = graphspace.get_shared_graph_layouts(graph_id=graph_id)
	assert all(isinstance(x, Layout) for x in layouts)
	assert len(layouts) >= 0


def test_post_graph_layout(graph_id, name=None):
	graphspace = GraphSpace('user1@example.com', 'user1')
	layout1 = GSLayout()
	if name is not None:
		layout1.set_name(name)
	layout1.set_node_position('a',45,55)
	layout1.set_node_position('b',36,98)
	layout1.add_node_style('a', shape='ellipse', color='green', width=90, height=90)
	layout1.add_node_style('b', shape='ellipse', color='yellow', width=40, height=40)
	layout = graphspace.post_graph_layout(graph_id=graph_id, layout=layout1)
	assert type(layout) is Layout
	assert layout.get_name() == layout1.get_name()
	return layout


def test_get_graph_layout(graph_id, name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	layout = graphspace.get_graph_layout(graph_id=graph_id, layout_name=name)
	assert type(layout) is Layout
	assert layout.get_name() == name


def test_update_graph_layout(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	layout = graphspace.get_graph_layout(graph_id=graph_id, layout_id=layout_id)
	layout.set_node_position('z',74,37)
	layout.set_is_shared()
	layout1 = graphspace.update_graph_layout(layout)
	assert type(layout1) is Layout
	assert layout1.get_name() == layout.get_name()
	assert 'z' in layout1.positions_json
	assert layout1.is_shared == 1


def test_update_graph_layout2(graph_id, name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	L = GSLayout()
	L.set_node_position('b', y=38.5, x=67.3)
	L.set_node_position('a', y=102, x=238.1)
	L.add_node_style('a', shape='octagon', color='green', width=60, height=60)
	L.add_edge_style('a', 'b', directed=True, edge_style='solid')
	L.set_name(name)
	L.set_is_shared()
	layout = graphspace.update_graph_layout(graph_id=graph_id, layout=L)
	assert type(layout) is Layout
	assert layout.get_name() == L.get_name()
	assert layout.is_shared == 1


def test_delete_graph_layout(graph_id, name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.delete_graph_layout(graph_id=graph_id, layout_name=name)
	assert graphspace.get_graph_layout(graph_id=graph_id, layout_name=name) is None
