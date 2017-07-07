import pytest
from graphspace_python.graphs.classes.gsgroup import GSGroup
from graphspace_python.api.client import GraphSpace
from graphspace_python.api.obj.api_response import APIResponse
from graphspace_python.api import errors


def test_groups_endpoint(graph_id):
	group = test_post_group(name='MyTestGroup')
	test_group_already_exists_error(name='MyTestGroup')
	test_get_group(name='MyTestGroup')
	test_update_group(name='MyTestGroup')
	test_get_my_groups()
	test_get_all_groups()
	test_get_group_members(name='MyTestGroup')
	member = test_add_group_member(member_email='user3@example.com', group_id=group.id)
	test_user_already_exists_error(member_email='user3@example.com', group_id=group.id)
	test_user_doesnt_exist_error(member_email='user5@example.com', group_id=group.id)
	test_delete_group_member(member_id=member['user_id'], group_id=group.id)
	test_member_doesnt_exist_error(member_id=member['user_id'], group_id=group.id)
	test_get_group_graphs(name='MyTestGroup')
	test_add_group_graph(graph_id=graph_id, name='MyTestGroup')
	test_graph_already_exists_for_group_error(graph_id=graph_id, name='MyTestGroup')
	test_delete_group_graph(graph_id=graph_id, name='MyTestGroup')
	test_graph_doesnt_exist_for_group_error(graph_id=graph_id, name='MyTestGroup')
	test_delete_group(name='MyTestGroup')
	test_user_not_authorised_error(group_id=group.id)


def test_group_already_exists_error(name):
	with pytest.raises(errors.BadRequest) as err:
		test_post_graph(name=name)


def test_user_already_exists_error(member_email, group_id):
	with pytest.raises(errors.UserAlreadyExists) as err:
		test_add_group_member(member_email=member_email, group_id=group_id)


def test_user_doesnt_exist_error(member_email, group_id):
	with pytest.raises(errors.BadRequest) as err:
		test_add_group_member(member_email=member_email, group_id=group_id)
        assert err.error_message == "User does not exit."


def test_member_doesnt_exist_error(member_id, group_id):
	with pytest.raises(errors.BadRequest) as err:
		test_delete_group_member(member_id=member_id, group_id=group_id)


def test_graph_already_exists_for_group_error(graph_id, group_id):
	with pytest.raises(errors.BadRequest) as err:
		test_add_group_graph(graph_id=graph_id, group_id=group_id)


def test_graph_doesnt_exist_for_group_error(graph_id, group_id):
	with pytest.raises(errors.BadRequest) as err:
		test_delete_group_graph(graph_id=graph_id, group_id=group_id)


def test_user_not_authorised_error(group_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	with pytest.raises(errors.UserNotAuthorised) as err:
		graphspace.get_group(group_id=group_id)


def test_update_group(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	group = graphspace.get_group(name=name).group
	group.set_description('A sample group for testing purpose')
	response = graphspace.update_group(group, name=name)
	assert type(response) is APIResponse
	assert hasattr(response, 'group') and response.group.get_description() == group.get_description()


def test_delete_group(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	graphspace.delete_group(name=name)
	assert graphspace.get_group(name=name) is None


def test_post_group(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	group = GSGroup(name, 'Sample group')
	response = graphspace.post_group(group)
	assert type(response) is APIResponse
	assert hasattr(response, 'group') and response.group.get_name() == group.get_name()
	return response.group


def test_get_group(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_group(name=name)
	assert type(response) is APIResponse
	assert hasattr(response, 'group') and response.group.name == name


def test_get_my_groups():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_my_groups()
	assert type(response) is APIResponse
	assert hasattr(response, 'groups') and len(response.groups) > 0


def test_get_all_groups():
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_all_groups()
	assert type(response) is APIResponse
	assert hasattr(response, 'groups') and len(response.groups) > 0


def test_get_group_members(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_group_members(name=name)
	assert type(response) is APIResponse
	assert hasattr(response, 'members') and len(response.members) > 0


def test_add_group_member(member_email, group_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.add_group_member(member_email, group_id=group_id)
	assert 'user_id' in response.keys()
	assert 'group_id' in response.keys() and response['group_id'] == str(group_id)


def test_delete_group_member(member_id, group_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.delete_group_member(member_id, group_id=group_id)
	assert response == "Successfully deleted member with id=%s from group with id=%s" % (member_id, group_id)


def test_get_group_graphs(name):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_group_graphs(name=name)
	assert type(response) is APIResponse
	assert hasattr(response, 'graphs') and len(response.graphs) >= 0


def test_add_group_graph(graph_id, group_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.add_group_graph(graph_id, group_id=group_id)
	assert 'graph_id' in response.keys() and response['graph_id'] == graph_id
	assert 'group_id' in response.keys() and response['group_id'] == str(group_id)


def test_delete_group_graph(graph_id, group_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.delete_group_graph(graph_id, group_id=group_id)
	assert response == "Successfully deleted graph with id=%s from group with id=%s" % (graph_id, group_id)
