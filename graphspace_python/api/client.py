import base64

import requests
import six
import urllib


class GraphSpace:
	API_HOST = 'www.graphspace.org'

	def __init__(self, username, password):
		self.auth_token = 'Basic %s' % base64.b64encode('{0}:{1}'.format(username, password))
		self.username = username
		self.api_host = GraphSpace.API_HOST

	def set_api_host(self, host):
		self.api_host = host

	def _make_request(self, method, path, url_params={}, data={}, headers=None):
		if headers is None:
			headers = {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'Authorization': self.auth_token
			}

		if method == "GET":
			return requests.get('http://{0}{1}?{2}'.format(
				self.api_host,
				six.moves.urllib.parse.quote(path.encode('utf-8')),
				urllib.urlencode(url_params, doseq=True)
			), headers=headers)
		elif method == "POST":
			return requests.post('http://{0}{1}?{2}'.format(
				self.api_host,
				six.moves.urllib.parse.quote(path.encode('utf-8')),
				urllib.urlencode(url_params)
			), json=data, headers=headers)
		elif method == "PUT":
			return requests.put('http://{0}{1}?{2}'.format(
				self.api_host,
				six.moves.urllib.parse.quote(path.encode('utf-8')),
				urllib.urlencode(url_params)
			), json=data, headers=headers)
		elif method == "DELETE":
			return requests.delete('http://{0}{1}?{2}'.format(
				self.api_host,
				six.moves.urllib.parse.quote(path.encode('utf-8')),
				urllib.urlencode(url_params)
			), headers=headers)

	def post_graph(self, graph, is_public=0):
		"""
		Posts NetworkX graph to the requesting users account on GraphSpace.

		:param graph: GSGraph object.
		:param is_public: 1 if graph is public else 0
		:return: Graph Object
		"""

		return self._make_request("POST", '/api/v1/graphs/',
		                          data={
			                          'name': graph.get_name(),
			                          'is_public': 0 if is_public is None else is_public,
			                          'owner_email': self.username,
			                          'graph_json': graph.compute_graph_json(),
			                          'style_json': graph.get_style_json()
		                          }).json()

	def get_graph(self, name, owner_email=None):
		"""
		Get a graph owned by requesting user with the given name.

		:return: Graph Object if a graph with given name exists otherwise None.
		"""
		response = self._make_request("GET", '/api/v1/graphs/', url_params={
			'owner_email': self.username if owner_email is None else owner_email,
			'names[]': name
		}).json()

		if response.get('total', 0) > 0:
			return response.get('graphs')[0]
		else:
			return None

	def get_public_graphs(self, tags=None, limit=20, offset=0):
		"""
		Get public graphs.

		:param tags: Search for graphs with the given given list of tag names. In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol. For example, %xyz% will search for all graphs with 'xyz' in their tag names.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: List of Graphs
		"""
		query = {
			'is_public': 1,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return self._make_request("GET", '/api/v1/graphs/', url_params=query).json()

	def get_shared_graphs(self, tags=None, limit=20, offset=0):
		"""
		Get shared graphs.

		:param tags: Search for graphs with the given given list of tag names. In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol. For example, %xyz% will search for all graphs with 'xyz' in their tag names.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: List of Graphs
		"""
		query = {
			'member_email': self.username,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return self._make_request("GET", '/api/v1/graphs/', url_params=query).json()

	def get_my_graphs(self, tags=None, limit=20, offset=0):
		"""
		Get my graphs.

		:param tags: Search for graphs with the given given list of tag names. In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol. For example, %xyz% will search for all graphs with 'xyz' in their tag names.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: List of Graphs
		"""
		query = {
			'owner_email': self.username,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return self._make_request("GET", '/api/v1/graphs/', url_params=query).json()

	def delete_graph(self, name):
		"""
		Delete a graph with given name.

		:param name: Name of the graph

		:return: Success Message from GraphSpace
		"""
		graph = self.get_graph(name)
		if graph is None or 'id' not in graph:
			raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.username))
		else:
			return self._make_request("DELETE", '/api/v1/graphs/' + str(graph['id'])).json()

	def update_graph(self, name, owner_email=None, graph=None, is_public=None):
		"""
		Update a graph with given name.

		:param name: Name of the graph
		:param graph: GSGraph object.
		:param is_public: 1 if graph is public else 0

		:return: Graph
		"""
		if graph is not None:
			data = {
				'name': graph.get_name(),
				'is_public': 0 if is_public is None else is_public,
				'graph_json': graph.compute_graph_json(),
				'style_json': graph.get_style_json()
			}
		else:
			data = {
				'is_public': 0 if is_public is None else is_public,
			}

		graph = self.get_graph(name, owner_email=owner_email)
		if graph is None or 'id' not in graph:
			raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.username))
		else:
			return self._make_request("PUT", '/api/v1/graphs/' + str(graph['id']), data=data).json()

	def make_graph_public(self, name):
		"""
		Makes a graph publicly viewable.

		:param name: Name of the graph.
		:return: Graph
		"""

		return self.update_graph(name, is_public=1)

	def make_graph_private(self, name):
		"""
		Makes a graph privately viewable.

		:param name: Name of the graph.
		:return: Graph
		"""
		return self.update_graph(name, is_public=0)
