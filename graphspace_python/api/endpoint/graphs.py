from graphspace_python.api.config import GRAPHS_PATH
from graphspace_python.api.obj.api_response import APIResponse

class Graphs(object):
	"""Graphs endpoint class.

	Provides methods for graph related operations such as saving, fetching, updating and deleting graphs on GraphSpace.
	"""

	def __init__(self, client):
		self.client = client

	def post_graph(self, graph):
		"""Posts NetworkX graph to the requesting users account on GraphSpace.

		Args:
			graph (GSGraph or Graph): Object having graph details, such as name, graph_json, style_json, is_public, tags.

		Returns:
			Graph: Saved graph on GraphSpace.
		"""
		data = graph.json()
		data.update({'owner_email': self.client.username})
		return APIResponse('graph',
			self.client._make_request("POST", GRAPHS_PATH, data=data)
		).graph

	def get_graph(self, name=None, graph_id=None, owner_email=None):
		"""Get a graph with the given name or graph_id.

		Args:
			name (str, optional): Name of the graph to be fetched. Defaults to None.
			graph_id (int, optional): ID of the graph to be fetched. Defaults to None.
			owner_email (str, optional): Email of the owner of the graph. Defaults to None.

		Returns:
			Graph or None: Graph object, if graph with the given 'name' or 'graph_id' exists; otherwise None.

		Raises:
			Exception: If both 'name' and 'graph_id' are None.
		"""
		if graph_id is not None:
			graph_by_id_path = GRAPHS_PATH + str(graph_id)
			return APIResponse('graph',
				self.client._make_request("GET", graph_by_id_path)
			).graph

		if name is not None:
			query = {
				'owner_email': self.client.username if owner_email is None else owner_email,
				'names[]': name
			}
			if owner_email is not None and owner_email != self.client.username:
				query.update({'is_public': 1})
			response = self.client._make_request("GET", GRAPHS_PATH, url_params=query)
			if response.get('total', 0) > 0:
				return APIResponse('graph',
					response.get('graphs')[0]
				).graph
			else:
				return None

		raise Exception('Both graph_id and name can\'t be none!')

	def get_public_graphs(self, tags=None, limit=20, offset=0):
		"""Get public graphs.

		Args:
			tags (List[str], optional): Search for graphs with the given given list of tag names.
				In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol.
				For example, %xyz% will search for all graphs with 'xyz' in their tag names. Defaults to None.
			offset (int, optional): Offset the list of returned entities by this number. Defaults to 0.
			limit (int, optional): Number of entities to return. Defaults to 20.

		Returns:
		 	List[Graph]: List of public graphs.
		"""
		query = {
			'is_public': 1,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return APIResponse('graph',
			self.client._make_request("GET", GRAPHS_PATH, url_params=query)
		).graphs

	def get_shared_graphs(self, tags=None, limit=20, offset=0):
		"""Get graphs shared with the groups where requesting user is a member.

		Args:
			tags (List[str], optional): Search for graphs with the given given list of tag names.
				In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol.
				For example, %xyz% will search for all graphs with 'xyz' in their tag names. Defaults to None.
			offset (int, optional): Offset the list of returned entities by this number. Defaults to 0.
			limit (int, optional): Number of entities to return. Defaults to 20.

		Returns:
		 	List[Graph]: List of shared graphs.
		"""
		query = {
			'member_email': self.client.username,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return APIResponse('graph',
			self.client._make_request("GET", GRAPHS_PATH, url_params=query)
		).graphs

	def get_my_graphs(self, tags=None, limit=20, offset=0):
		"""Get graphs created by the requesting user.

		Args:
			tags (List[str], optional): Search for graphs with the given given list of tag names.
				In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol.
				For example, %xyz% will search for all graphs with 'xyz' in their tag names. Defaults to None.
			offset (int, optional): Offset the list of returned entities by this number. Defaults to 0.
			limit (int, optional): Number of entities to return. Defaults to 20.

		Returns:
		 	List[Graph]: List of graphs owned by the requesting user.
		"""
		query = {
			'owner_email': self.client.username,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return APIResponse('graph',
			self.client._make_request("GET", GRAPHS_PATH, url_params=query)
		).graphs

	def delete_graph(self, name=None, graph_id=None):
		"""Delete a graph with the given name or graph_id.

		Args:
			name (str, optional): Name of the graph to be deleted. Defaults to None.
			graph_id (int, optional): ID of the graph to be deleted. Defaults to None.

		Returns:
		 	str: Success/Error Message from GraphSpace.

		Raises:
			Exception: If both 'name' and 'graph_id' are None or if graph doesnot exist.
		"""
		if graph_id is not None:
			graph_by_id_path = GRAPHS_PATH + str(graph_id)
			response = self.client._make_request("DELETE", graph_by_id_path)
			return response['message']

		if name is not None:
			response = self.get_graph(name=name)
			if response is None or response.graph.id is None:
				raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				graph_by_id_path = GRAPHS_PATH + str(response.graph.id)
				response = self.client._make_request("DELETE", graph_by_id_path)
				return response['message']

		raise Exception('Both graph_id and name can\'t be none!')

	def update_graph(self, graph, name=None, graph_id=None, owner_email=None):
		"""Update a graph with the given name or graph_id.

		Args:
			graph (GSGraph or Graph): Object having graph details, such as name, graph_json, style_json, is_public, tags.
			name (str, optional): Name of the graph to be updated. Defaults to None.
			graph_id (int, optional): ID of the graph to be updated. Defaults to None.
			owner_email (str, optional): Email of owner of the graph. Defaults to None.

		Returns:
		 	Graph: Updated graph on GraphSpace.

		Raises:
			Exception: If both 'name' and 'graph_id' are None or if graph doesnot exist.
		"""
		if graph_id is not None:
			graph_by_id_path = GRAPHS_PATH + str(graph_id)
			return APIResponse('graph',
				self.client._make_request("PUT", graph_by_id_path, data=graph.json())
			).graph

		if name is not None:
			response = self.get_graph(name=name, owner_email=owner_email)
			if response is None or response.graph.id is None:
				raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				graph_by_id_path = GRAPHS_PATH + str(response.graph.id)
				return APIResponse('graph',
					self.client._make_request("PUT", graph_by_id_path, data=graph.json())
				).graph

		raise Exception('Both graph_id and name can\'t be none!')

	def make_graph_public(self, name=None, graph_id=None):
		"""Makes a graph publicly viewable.

		Args:
			name (str, optional): Name of the graph. Defaults to None.
			graph_id (int, optional): ID of the graph. Defaults to None.

		Returns:
		 	Graph: Updated graph on GraphSpace.

		Raises:
			Exception: If both 'name' and 'graph_id' are None or if graph doesnot exist.
		"""
		if graph_id is not None:
			graph_by_id_path = GRAPHS_PATH + str(graph_id)
			return APIResponse('graph',
				self.client._make_request("PUT", graph_by_id_path, data={'is_public': 1})
			).graph

		if name is not None:
			response = self.get_graph(name=name)
			if response is None or response.graph.id is None:
				raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				graph_by_id_path = GRAPHS_PATH + str(response.graph.id)
				return APIResponse('graph',
					self.client._make_request("PUT", graph_by_id_path, data={'is_public': 1})
				).graph

		raise Exception('Both graph_id and name can\'t be none!')

	def make_graph_private(self, name=None, graph_id=None):
		"""Makes a graph privately viewable.

		Args:
			name (str, optional): Name of the graph. Defaults to None.
			graph_id (int, optional): ID of the graph. Defaults to None.

		Returns:
		 	Graph: Updated graph on GraphSpace.

		Raises:
			Exception: If both 'name' and 'graph_id' are None or if graph doesnot exist.
		"""
		if graph_id is not None:
			graph_by_id_path = GRAPHS_PATH + str(graph_id)
			return APIResponse('graph',
				self.client._make_request("PUT", graph_by_id_path, data={'is_public': 0})
			).graph

		if name is not None:
			response = self.get_graph(name=name)
			if response is None or response.graph.id is None:
				raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
			else:
				graph_by_id_path = GRAPHS_PATH + str(response.graph.id)
				return APIResponse('graph',
					self.client._make_request("PUT", graph_by_id_path, data={'is_public': 0})
				).graph

		raise Exception('Both graph_id and name can\'t be none!')
