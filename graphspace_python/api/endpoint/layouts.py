from graphspace_python.api.config import LAYOUTS_PATH
from graphspace_python.api.obj.layout_response import LayoutResponse

class Layouts(object):
	"""Layouts endpoint Class
	"""

	def __init__(self, client):
		self.client = client

	def post_graph_layout(self, graph_id, layout):
		"""Create a layout for the graph with given graph_id.

		:param graph_id: ID of the graph.
		:param layout: GSLayout object.
		:return: LayoutResponse object that wraps the response.
		"""
		layouts_path = LAYOUTS_PATH.format(graph_id)
		return LayoutResponse(
			self.client._make_request("POST", layouts_path,
				data=layout.json().update({'graph_id': graph_id, 'owner_email': self.client.username}))
		)

	def update_graph_layout(self, graph_id, layout_id, layout):
		"""Update layout with given layout_id for the graph with given graph_id.

		:param layout_id: ID of the layout.
		:param graph_id: ID of the graph.
		:param layout: GSLayout object.
		:return: LayoutResponse object that wraps the response.
		"""
		layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
		return LayoutResponse(
			self.client._make_request("PUT", layout_by_id_path, data=layout.json())
		)

	def delete_graph_layout(self, graph_id, layout_id):
		"""Delete the given layout for the graph.

		:param graph_id: ID of the graph.
		:param layout_id: ID of the layout.
		:return: Success/Error Message from GraphSpace
		"""
		layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
		response = self.client._make_request("DELETE", layout_by_id_path)
		return response['message']

	def get_graph_layout(self, graph_id, layout_id):
		"""Get the given layout for the graph.

		:param graph_id: ID of the graph.
		:param layout_id: ID of the layout.
		:return: LayoutResponse object that wraps the response.
		"""
		layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
		return LayoutResponse(
			self.client._make_request("GET", layout_by_id_path)
		)

	def get_my_graph_layouts(self, graph_id, limit=20, offset=0):
		"""Get layouts created by the requesting user for the graph with given graph_id

		:param graph_id: ID of the graph.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: LayoutResponse object that wraps the response.
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'owner_email': self.client.username
		}

		layouts_path = LAYOUTS_PATH.format(graph_id)
		return LayoutResponse(
			self.client._make_request("GET", layouts_path, url_params=query)
		)

	def get_shared_graph_layouts(self, graph_id, limit=20, offset=0):
		"""Get layouts shared with the requesting user for the graph with given graph_id .

		:param graph_id: ID of the graph.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: LayoutResponse object that wraps the response.
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'is_shared': 1
		}

		layouts_path = LAYOUTS_PATH.format(graph_id)
		return LayoutResponse(
			self.client._make_request("GET", layouts_path, url_params=query)
		)
