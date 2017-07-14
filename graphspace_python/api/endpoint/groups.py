from graphspace_python.api.config import GROUPS_PATH
from graphspace_python.api.obj.api_response import APIResponse

class Groups(object):
	"""Groups endpoint class.

	Provides methods for group related operations such as saving, fetching, updating, deleting groups on GraphSpace.

	Also provides methods for group member and group graph related operations such as fetching
	all members or graphs of the group, adding or deleting new member or graph to the group.
	"""

	def __init__(self, client):
		self.client = client

	def post_group(self, group):
		"""Create a group for the requesting user.

		Args:
			group (GSGroup or Group): Object having group details, such as name, description.

		Returns:
		 	Group: Saved group on GraphSpace.
		"""
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		data = group.json()
		data.update({'owner_email': self.client.username})
		return APIResponse('group',
			self.client._make_request("POST", GROUPS_PATH, data=data, headers=headers)
		).group

	def get_group(self, name=None, group_id=None):
		"""Get a group with the given name or group_id, where the requesting user is a member.

		Args:
			name (str, optional): Name of the group to be fetched. Defaults to None.
			group_id (int, optional): ID of the group to be fetched. Defaults to None.

		Returns:
		 	Group or None: Group object, if group with the given 'name' or 'group_id' exists; otherwise None.

		Raises:
			Exception: If both 'name' and 'group_id' are None.
		"""
		if group_id is not None:
			group_by_id_path = GROUPS_PATH + str(group_id)
			return APIResponse('group',
				self.client._make_request("GET", group_by_id_path)
			).group

		if name is not None:
			response = self.client._make_request("GET", GROUPS_PATH, url_params={
				'member_email': self.client.username,
				'name': name
			})
			if response.get('total', 0) > 0:
				return APIResponse('group',
					response.get('groups')[0]
				).group
			else:
				return None

		raise Exception('Both group_id and name can\'t be none!')

	def update_group(self, group, name=None, group_id=None):
		"""Update a group with the given name or group_id, where the requesting user is the owner.

		Args:
			group (GSGroup or Group): Object having group details, such as name, description.
			name (str, optional): Name of the group to be updated. Defaults to None.
			group_id (int, optional): ID of the group to be updated. Defaults to None.

		Returns:
		 	Group: Updated group on GraphSpace.

		Raises:
			Exception: If both 'name' and 'group_id' are None or if group doesnot exist.
		"""
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		if group_id is not None:
			group_by_id_path = GROUPS_PATH + str(group_id)
			return APIResponse('group',
				self.client._make_request("PUT", group_by_id_path, data=group.json(), headers=headers)
			).group

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_by_id_path = GROUPS_PATH + str(response.group.id)
				return APIResponse('group',
					self.client._make_request("PUT", group_by_id_path, data=group.json(), headers=headers)
				).group

		raise Exception('Both group_id and name can\'t be none!')

	def delete_group(self, name=None, group_id=None):
		"""Delete a group with the given name or group_id, where the requesting user is the owner.

		Args:
			name (str, optional): Name of the group to be deleted. Defaults to None.
			group_id (int, optional): ID of the group to be deleted. Defaults to None.

		Returns:
		 	str: Success/Error Message from GraphSpace.

		Raises:
			Exception: If both 'name' and 'group_id' are None or if group doesnot exist.
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

		Args:
			offset (int, optional): Offset the list of returned entities by this number. Defaults to 0.
			limit (int, optional): Number of entities to return. Defaults to 20.

		Returns:
			List[Group]: List of groups owned by the requesting user.
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'owner_email': self.client.username
		}

		return APIResponse('group',
			self.client._make_request("GET", GROUPS_PATH, url_params=query)
		).groups

	def get_all_groups(self, limit=20, offset=0):
		"""Get groups where the requesting user is a member.

		Args:
			offset (int, optional): Offset the list of returned entities by this number. Defaults to 0.
			limit (int, optional): Number of entities to return. Defaults to 20.

		Returns:
		 	List[Group]: List of groups where the requesting user is a member.
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'member_email': self.client.username
		}

		return APIResponse('group',
			self.client._make_request("GET", GROUPS_PATH, url_params=query)
		).groups

	def get_group_members(self, name=None, group_id=None):
		"""Get members of a group with given group_id or name.

		Args:
			name (str, optional): Name of the group. Defaults to None.
			group_id (int, optional): ID of the group. Defaults to None.

		Returns:
			List[Member]: List of members belonging to the group.

		Raises:
			Exception: If both 'name' and 'group_id' are None or if group doesnot exist.
		"""
		if group_id is not None:
			group_members_path = GROUPS_PATH + str(group_id) + '/members'
			return APIResponse('member',
				self.client._make_request("GET", group_members_path)
			).members

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_members_path = GROUPS_PATH + str(response.group.id) + '/members'
				return APIResponse('member',
					self.client._make_request("GET", group_members_path)
				).members

		raise Exception('Both group_id and name can\'t be none!')

	def add_group_member(self, member_email, name=None, group_id=None):
		"""Add a member to a group with given group_id or name.

		Args:
			member_email (str): Email of the member to be added to the group.
			name (str, optional): Name of the group. Defaults to None.
			group_id (int, optional): ID of the group. Defaults to None.

		Returns:
			dict: Dict containing 'group_id' and 'user_id' of the added member.

		Raises:
			Exception: If both 'name' and 'group_id' are None or if group doesnot exist.
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

		Args:
			member_id (int): ID of the member to be deleted from the group.
			name (str, optional): Name of the group. Defaults to None.
			group_id (int, optional): ID of the group. Defaults to None.

		Returns:
		 	str: Success/Error Message from GraphSpace.

		Raises:
			Exception: If both 'name' and 'group_id' are None or if group doesnot exist.
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

		Args:
			name (str, optional): Name of the group. Defaults to None.
			group_id (int, optional): ID of the group. Defaults to None.

		Returns:
			List[Graph]: List of graphs belonging to the group.

		Raises:
			Exception: If both 'name' and 'group_id' are None or if group doesnot exist.
		"""
		if group_id is not None:
			group_graphs_path = GROUPS_PATH + str(group_id) + '/graphs'
			return APIResponse('graph',
				self.client._make_request("GET", group_graphs_path)
			).graphs

		if name is not None:
			response = self.get_group(name=name)
			if response is None or response.group.id is None:
				raise Exception('Group with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				group_graphs_path = GROUPS_PATH + str(response.group.id) + '/graphs'
				return APIResponse('graph',
					self.client._make_request("GET", group_graphs_path)
				).graphs

		raise Exception('Both group_id and name can\'t be none!')

	def add_group_graph(self, graph_id, name=None, group_id=None):
		"""Add a graph to a group with given group_id or name.

		Args:
			graph_id (int): ID of the graph to be added to the group.
			name (str, optional): Name of the group. Defaults to None.
			group_id (int, optional): ID of the group. Defaults to None.

		Returns:
			dict: Dict containing 'group_id', 'graph_id', 'created_at', 'updated_at' details of the added graph.

		Raises:
			Exception: If both 'name' and 'group_id' are None or if group doesnot exist.
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
				group_graphs_path = GROUPS_PATH + str(response.group.id) + '/graphs'
				return self.client._make_request("POST", group_graphs_path, data={'graph_id': graph_id}, headers=headers)

		raise Exception('Both group_id and name can\'t be none!')

	def delete_group_graph(self, graph_id, name=None, group_id=None):
		"""Delete a graph from a group with given group_id or name.

		Args:
			graph_id (int): ID of the group to be deleted from the group.
			name (str, optional): Name of the group. Defaults to None.
			group_id (int, optional): ID of the group. Defaults to None.

		Returns:
		 	str: Success/Error Message from GraphSpace.

		Raises:
			Exception: If both 'name' and 'group_id' are None or if group doesnot exist.
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
				group_graphs_path = GROUPS_PATH + str(response.group.id) + '/graphs/' + str(graph_id)
				response = self.client._make_request("DELETE", group_graphs_path)
				return response['message']

		raise Exception('Both group_id and name can\'t be none!')
