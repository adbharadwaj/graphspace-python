import base64
import requests
import six
from future.standard_library import install_aliases
install_aliases()


class GraphSpace:
	API_HOST = 'www.graphspace.org'

	def __init__(self, username, password):
		# self.auth_token = 'Basic %s' % base64.b64encode('{0}:{1}'.format(username, password))
		self.auth_token = requests.auth.HTTPBasicAuth(username, password)
		self.username = username
		self.api_host = GraphSpace.API_HOST

	def set_api_host(self, host):
		self.api_host = host

	def _make_request(self, method, path, url_params={}, data={}, headers=None):
		if headers is None:
			headers = {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			}

		if method == "GET":
			return requests.get('http://{0}{1}?{2}'.format(
				self.api_host,
				six.moves.urllib.parse.quote(path.encode('utf-8')),
				six.moves.urllib.parse.urlencode(url_params, doseq=True)
			), headers=headers, auth=self.auth_token)
		elif method == "POST":
			return requests.post('http://{0}{1}?{2}'.format(
				self.api_host,
				six.moves.urllib.parse.quote(path.encode('utf-8')),
				six.moves.urllib.parse.urlencode(url_params)
			), json=data, headers=headers, auth=self.auth_token)
		elif method == "PUT":
			return requests.put('http://{0}{1}?{2}'.format(
				self.api_host,
				six.moves.urllib.parse.quote(path.encode('utf-8')),
				six.moves.urllib.parse.urlencode(url_params)
			), json=data, headers=headers, auth=self.auth_token)
		elif method == "DELETE":
			return requests.delete('http://{0}{1}?{2}'.format(
				self.api_host,
				six.moves.urllib.parse.quote(path.encode('utf-8')),
				six.moves.urllib.parse.urlencode(url_params)
			), headers=headers, auth=self.auth_token)

	def post_graph(self, graph, is_public=0):
		"""Posts NetworkX graph to the requesting users account on GraphSpace.

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
		"""Get a graph owned by requesting user with the given name.

		:return: Dict with graph details if a graph with given name exists otherwise None.
		"""
		response = self._make_request("GET", '/api/v1/graphs/', url_params={
			'owner_email': self.username if owner_email is None else owner_email,
			'names[]': name
		}).json()

		if response.get('total', 0) > 0:
			return response.get('graphs')[0]
		else:
			return None

	def get_graph_by_id(self, graph_id):
		"""Get a graph by id.

		:return: Dict with graph details if a graph with given id exists otherwise None.
		"""
		return self._make_request("GET", '/api/v1/graphs/%s'% graph_id).json()

	def get_public_graphs(self, tags=None, limit=20, offset=0):
		"""Get public graphs.

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
		"""Get graphs shared with the groups where requesting user is a member.

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
		"""Get graphs created by the requesting user.

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
		"""Delete graph with the given name.

		:param name: Name of the graph

		:return: Success/Error Message from GraphSpace
		"""
		graph = self.get_graph(name)
		if graph is None or 'id' not in graph:
			raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.username))
		else:
			return self._make_request("DELETE", '/api/v1/graphs/' + str(graph['id'])).json()

	def update_graph(self, name, owner_email=None, graph=None, is_public=None):
		"""Update graph with the given name with given details.

		:param name: Name of the graph
		:param owner_email: Email of owner of the graph.
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
		"""Makes a graph publicly viewable.

		:param name: Name of the graph.
		:return: Graph
		"""

		return self.update_graph(name, is_public=1)

	def make_graph_private(self, name):
		"""Makes a graph privately viewable.

		:param name: Name of the graph.
		:return: Graph
		"""
		return self.update_graph(name, is_public=0)

	def post_graph_layout(self, graph_id, layout_name, positions_json=None, style_json=None, is_shared=None):
		"""Create a layout for the graph with given graph_id.

		:param style_json: JSON containing style information about nodes.
		:param positions_json: JSON containing layout positions for the nodes.
		:param graph_id: ID of the graph.
		:param layout_name: Name of the layout.
		:param is_shared: 1 if layout is shared else 0
		:return: Layout Object

		Sample style_json::

			{
			    "style": [
			        {
			            "selector": "node[name='P4314611']",
			            "style": {
			                "border-color": "#888",
			                "text-halign": "center",
			                "text-valign": "center",
			                "border-width": "2px",
			                "height": "50px",
			                "width": "50px",
			                "shape": "ellipse",
			                "background-blacken": "0.1",
			                "background-color": "yellow"
			            }
			        },
			        {
			            "selector": "node[name='P0810711']",
			            "style": {
			                "text-halign": "center",
			                "text-valign": "center",
			                "text-outline-color": "#888",
			                "text-outline-width": "2px",
			                "border-color": "black",
			                "border-width": "5px",
			                "height": "150px",
			                "shape": "ellipse",
			                "color": "black",
			                "border-style": "double",
			                "text-wrap": "wrap",
			                "background-blacken": "0",
			                "width": "150px",
			                "background-color": "red"
			            }
			        },
			        {
			            "selector": "edge[name='P4314611-P0810711']",
			            "style": {
			                "curve-style": "bezier",
			                "line-style": "dotted",
			                "width": "12px",
			                "line-color": "blue",
			                "source-arrow-color": "yellow",
			                "target-arrow-shape": "triangle"
			            }
			        }
			    ]
			}

		Sample positions_json::

			{
			    "P4314611": {
			        "y": 87,
			        "x": 35
			    },
			    "P0810711": {
			        "y": 87.89306358381505,
			        "x": 208.18593448940268
			    }
			}


		"""
		data = {
			'name': layout_name,
			'graph_id': graph_id,
			'is_shared': 0 if is_shared is None else is_shared,
			'owner_email': self.username
		}

		if positions_json is not None:
			data.update({'positions_json': positions_json})
		else:
			data.update({'positions_json': {}})
		if style_json is not None:
			data.update({'style_json': style_json})
		else:
			data.update({'style_json': {'style': []}})

		return self._make_request("POST", '/api/v1/graphs/%s/layouts/' % graph_id, data=data).json()

	def update_graph_layout(self, graph_id, layout_id, layout_name=None, positions_json=None, style_json=None, is_shared=None):
		"""Update layout with given layout_id for the graph with given graph_id.

		:param layout_id: ID of the layout.
		:param style_json: JSON containing style information about nodes.
		:param positions_json: JSON containing layout positions for the nodes.
		:param graph_id: ID of the graph.
		:param layout_name: Name of the layout.
		:param is_shared: 1 if layout is shared else 0
		:return: Layout Object

		Sample style_json::

			{
			    "style": [
			        {
			            "selector": "node[name='P4314611']",
			            "style": {
			                "border-color": "#888",
			                "text-halign": "center",
			                "text-valign": "center",
			                "border-width": "2px",
			                "height": "50px",
			                "width": "50px",
			                "shape": "ellipse",
			                "background-blacken": "0.1",
			                "background-color": "yellow"
			            }
			        },
			        {
			            "selector": "node[name='P0810711']",
			            "style": {
			                "text-halign": "center",
			                "text-valign": "center",
			                "text-outline-color": "#888",
			                "text-outline-width": "2px",
			                "border-color": "black",
			                "border-width": "5px",
			                "height": "150px",
			                "shape": "ellipse",
			                "color": "black",
			                "border-style": "double",
			                "text-wrap": "wrap",
			                "background-blacken": "0",
			                "width": "150px",
			                "background-color": "red"
			            }
			        },
			        {
			            "selector": "edge[name='P4314611-P0810711']",
			            "style": {
			                "curve-style": "bezier",
			                "line-style": "dotted",
			                "width": "12px",
			                "line-color": "blue",
			                "source-arrow-color": "yellow",
			                "target-arrow-shape": "triangle"
			            }
			        }
			    ]
			}

		Sample positions_json::

			{
			    "P4314611": {
			        "y": 87,
			        "x": 35
			    },
			    "P0810711": {
			        "y": 87.89306358381505,
			        "x": 208.18593448940268
			    }
			}

		"""
		data = {}

		if layout_name is not None:
			data.update({'name': layout_name})
		if is_shared is not None:
			data.update({'is_shared': is_shared})
		if positions_json is not None:
			data.update({'positions_json': positions_json})
		if style_json is not None:
			data.update({'style_json': style_json})

		return self._make_request("PUT", '/api/v1/graphs/%s/layouts/%s' % (graph_id, layout_id), data=data).json()

	def delete_graph_layout(self, graph_id, layout_id):
		"""Delete the given layout for the graph.

		:param graph_id: ID of the graph.
		:param layout_id: ID of the layout.
		:return: Response
		"""

		return self._make_request("DELETE", '/api/v1/graphs/%s/layouts/%s' % (graph_id, layout_id)).json()

	def get_graph_layout(self, graph_id, layout_id):
		"""Get the given layout for the graph.

		:param graph_id: ID of the graph.
		:param layout_id: ID of the layout.
		:return: Layout object
		"""

		response = self._make_request("GET", '/api/v1/graphs/%s/layouts/%s' % (graph_id, layout_id)).json()
		return None if 'id' not in response else response

	def get_my_graph_layouts(self, graph_id, limit=20, offset=0):
		"""Get layouts created by the requesting user for the graph with given graph_id

		:param graph_id: Id of the graph.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: List of layouts
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'owner_email': self.username
		}

		return self._make_request("GET", '/api/v1/graphs/%s/layouts/' % graph_id, url_params=query).json()

	def get_shared_graph_layouts(self, graph_id, limit=20, offset=0):
		"""Get layouts shared with the requesting user for the graph with given graph_id .

		:param graph_id: Id of the graph.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: List of layouts
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'is_shared': 1
		}

		return self._make_request("GET", '/api/v1/graphs/%s/layouts/' % graph_id, url_params=query).json()
