from graphspace_python.api.config import GROUPS_PATH
from graphspace_python.api.obj.api_response import APIResponse

class Groups(object):
	"""Groups Endpoint Class
	"""

	def __init__(self, client):
		self.client = client

	def post_group(self, group):
		"""Create a group for the requesting user.

		:param graph: GSGroup object.
		:return: GroupResponse object that wraps the response.
		"""
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		data = group.json()
		data.update({'owner_email': self.client.username})
		return APIResponse('group',
			self.client._make_request("POST", GROUPS_PATH, data=data, headers=headers)
		)

	def get_group(self, name=None, group_id=None):
		"""Get a group with the given name or group_id, where the requesting user is a member.

		:param name: Name of the group to be searched.
		:param id: ID of the group to be searched.
		:return: GroupResponse object that wraps the response.
		"""
		if group_id is not None:
			group_by_id_path = GROUPS_PATH + str(group_id)
			return APIResponse('group',
				self.client._make_request("GET", group_by_id_path)
			)

		if name is not None:
			response = self.client._make_request("GET", GROUPS_PATH, url_params={
				'member_email': self.client.username,
				'name': name
			})
			if response.get('total', 0) > 0:
				return APIResponse('group',
					response.get('groups')[0]
				)
			else:
				return None

		raise Exception('Both group_id and name can\'t be none!')

	def update_group(self, group, name=None, group_id=None):
		"""Update a group with the given name or group_id, where the requesting user is the owner.

		:param group: GSGroup object.
		:param name: Name of the group to be updated.
		:param id: ID of the group to be updated.
		:return: GroupResponse object that wraps the response.
		"""
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		if group_id is not None:
			group_by_id_path = GROUPS_PATH + str(group_id)
			return APIResponse('group',
				self.client._make_request("PUT", group_by_id_path, data=group.json(), headers=headers)
			)

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_by_id_path = GROUPS_PATH + str(response.group.id)
				return APIResponse('group',
					self.client._make_request("PUT", group_by_id_path, data=group.json(), headers=headers)
				)

		raise Exception('Both group_id and name can\'t be none!')

	def delete_group(self, name=None, group_id=None):
		"""Delete a group with the given name or group_id, where the requesting user is the owner.

		:param name: Name of the group to be deleted.
		:param id: ID of the group to be deleted.
		:return: Success/Error Message from GraphSpace.
		"""
		if group_id is not None:
			group_by_id_path = GROUPS_PATH + str(group_id)
			response = self.client._make_request("DELETE", group_by_id_path)
			return response['message']

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_by_id_path = GROUPS_PATH + str(response.group.id)
				response = self.client._make_request("DELETE", group_by_id_path)
				return response['message']

		raise Exception('Both group_id and name can\'t be none!')

	def get_my_groups(self, limit=20, offset=0):
		"""Get groups created by the requesting user.

		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: GroupResponse object that wraps the response.
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'owner_email': self.client.username
		}

		return APIResponse('group',
			self.client._make_request("GET", GROUPS_PATH, url_params=query)
		)

	def get_all_groups(self, limit=20, offset=0):
		"""Get groups where the requesting user is a member.

		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: GroupResponse object that wraps the response.
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'member_email': self.client.username
		}

		return APIResponse('group',
			self.client._make_request("GET", GROUPS_PATH, url_params=query)
		)

	def get_group_members(self, name=None, group_id=None):
		"""Get members of a group with given group_id or name.

		:param name: Name of the group.
		:param group_id: ID of the group.
		:return: MemberResponse object that wraps the response.
		"""
		if group_id is not None:
			group_members_path = GROUPS_PATH + str(group_id) + '/members'
			return APIResponse('member',
				self.client._make_request("GET", group_members_path)
			)

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_members_path = GROUPS_PATH + str(response.group.id) + '/members'
				return APIResponse('member',
					self.client._make_request("GET", group_members_path)
				)

		raise Exception('Both group_id and name can\'t be none!')

	def add_group_member(self, member_email, name=None, group_id=None):
		"""Add a member to a group with given group_id or name.

		:param member_email: Email of the member to be added to the group.
		:param name: Name of the group.
		:param group_id: ID of the group.
		:return: Dict containing group_id and member_id of the added member.
		"""
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		if group_id is not None:
			group_members_path = GROUPS_PATH + str(group_id) + '/members'
			return self.client._make_request("POST", group_members_path, data={'member_email': member_email}, headers=headers)

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_members_path = GROUPS_PATH + str(response.group.id) + '/members'
				return self.client._make_request("POST", group_members_path, data={'member_email': member_email}, headers=headers)

		raise Exception('Both group_id and name can\'t be none!')

	def delete_group_member(self, member_id, name=None, group_id=None):
		"""Delete a member from a group with given group_id or name.

		:param member_id: ID of the member to be deleted from the group.
		:param name: Name of the group.
		:param group_id: ID of the group.
		:return: Success/Error Message from GraphSpace.
		"""
		if group_id is not None:
			group_members_path = GROUPS_PATH + str(group_id) + '/members/' + str(member_id)
			response = self.client._make_request("DELETE", group_members_path)
			return response['message']

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_members_path = GROUPS_PATH + str(response.group.id) + '/members/' + str(member_id)
				response = self.client._make_request("DELETE", group_members_path)
				return response['message']

		raise Exception('Both group_id and name can\'t be none!')

	def get_group_graphs(self, name=None, group_id=None):
		"""Get graphs of a group with given group_id or name.

		:param name: Name of the group.
		:param group_id: ID of the group.
		:return: GraphResponse object that wraps the response.
		"""
		if group_id is not None:
			group_graphs_path = GROUPS_PATH + str(group_id) + '/graphs'
			return APIResponse('graph',
				self.client._make_request("GET", group_graphs_path)
			)

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_graphs_path = GROUPS_PATH + str(response.group.group_id) + '/graphs'
				return APIResponse('graph',
					self.client._make_request("GET", group_graphs_path)
				)

		raise Exception('Both group_id and name can\'t be none!')

	def add_group_graph(self, graph_id, name=None, group_id=None):
		"""Add a graph to a group with given group_id or name.

		:param graph_id: ID of the graph to be added to the group.
		:param name: Name of the group.
		:param group_id: ID of the group.
		:return: Dict containing group_id, graph_id and other details of the added graph.
		"""
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		if group_id is not None:
			group_graphs_path = GROUPS_PATH + str(group_id) + '/graphs'
			return self.client._make_request("POST", group_graphs_path, data={'graph_id': graph_id}, headers=headers)

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_graphs_path = GROUPS_PATH + str(response.group.group_id) + '/graphs'
				return self.client._make_request("POST", group_graphs_path, data={'graph_id': graph_id}, headers=headers)

		raise Exception('Both group_id and name can\'t be none!')

	def delete_group_graph(self, graph_id, name=None, group_id=None):
		"""Delete a graph from a group with given group_id or name.

		:param graph_id: ID of the group to be deleted from the group.
		:param name: Name of the group.
		:param group_id: ID of the group.
		:return: Success/Error Message from GraphSpace.
		"""
		if group_id is not None:
			group_graphs_path = GROUPS_PATH + str(group_id) + '/graphs/' + str(graph_id)
			response = self.client._make_request("DELETE", group_graphs_path)
			return response['message']

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_graphs_path = GROUPS_PATH + str(response.group.group_id) + '/graphs/' + str(graph_id)
				response = self.client._make_request("DELETE", group_graphs_path)
				return response['message']

		raise Exception('Both group_id and name can\'t be none!')
