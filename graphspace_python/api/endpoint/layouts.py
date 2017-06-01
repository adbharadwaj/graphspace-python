from graphspace_python.api.config import LAYOUTS_PATH

class Layouts(object):

	def __init__(self, client):
		self.client = client

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
			'owner_email': self.client.username
		}

		if positions_json is not None:
			data.update({'positions_json': positions_json})
		else:
			data.update({'positions_json': {}})
		if style_json is not None:
			data.update({'style_json': style_json})
		else:
			data.update({'style_json': {'style': []}})

		layouts_path = LAYOUTS_PATH.format(graph_id)
		return self.client._make_request("POST", layouts_path, data=data).json()

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

		layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
		return self.client._make_request("PUT", layout_by_id_path, data=data).json()

	def delete_graph_layout(self, graph_id, layout_id):
		"""Delete the given layout for the graph.

		:param graph_id: ID of the graph.
		:param layout_id: ID of the layout.
		:return: Response
		"""

		layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
		return self.client._make_request("DELETE", layout_by_id_path).json()

	def get_graph_layout(self, graph_id, layout_id):
		"""Get the given layout for the graph.

		:param graph_id: ID of the graph.
		:param layout_id: ID of the layout.
		:return: Layout object
		"""

		layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
		response = self.client._make_request("GET", layout_by_id_path).json()
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
			'owner_email': self.client.username
		}

		layouts_path = LAYOUTS_PATH.format(graph_id)
		return self.client._make_request("GET", layouts_path, url_params=query).json()

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

		layouts_path = LAYOUTS_PATH.format(graph_id)
		return self.client._make_request("GET", layouts_path, url_params=query).json()
