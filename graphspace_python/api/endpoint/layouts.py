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
		data = layout.json()
		data.update({'graph_id': graph_id, 'owner_email': self.client.username})
		layouts_path = LAYOUTS_PATH.format(graph_id)
		return LayoutResponse(
			self.client._make_request("POST", layouts_path, data=data)
		)

	def update_graph_layout(self, graph_id, layout, layout_id=None, name=None, owner_email=None):
		"""Update a layout with given layout_id or name for the graph with given graph_id.

		:param graph_id: ID of the graph.
		:param layout: GSLayout object.
		:param layout_id: ID of the layout.
		:param name: Name of the layout.
		:return: LayoutResponse object that wraps the response.
		"""
		if layout_id is not None:
			layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
			return LayoutResponse(
				self.client._make_request("PUT", layout_by_id_path, data=layout.json())
			)

		if name is not None:
			response = self.get_graph_layout(graph_id=graph_id, name=name, owner_email=owner_email)
			if response is None or response.layout.id is None:
				raise Exception('Layout with name `%s` of graph with graph_id=%s doesnt exist for user `%s`!' % (name, graph_id, self.client.username))
			else:
				layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(response.layout.id)
				return LayoutResponse(
					self.client._make_request("PUT", layout_by_id_path, data=layout.json())
				)

		raise Exception('Both layout_id and name can\'t be none!')

	def delete_graph_layout(self, graph_id, layout_id=None, name=None):
		"""Delete a layout with the given layout_id or name for the graph with given graph_id.

		:param graph_id: ID of the graph.
		:param layout_id: ID of the layout.
		:param name: Name of the layout.
		:return: Success/Error Message from GraphSpace
		"""
		if layout_id is not None:
			layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
			response = self.client._make_request("DELETE", layout_by_id_path)
			return response['message']

		if name is not None:
			response = self.get_graph_layout(graph_id=graph_id, name=name)
			if response is None or response.layout.id is None:
				raise Exception('Layout with name `%s` of graph with graph_id=%s doesnt exist for user `%s`!' % (name, graph_id, self.client.username))
			else:
				layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(response.layout.id)
				response = self.client._make_request("DELETE", layout_by_id_path)
				return response['message']

		raise Exception('Both layout_id and name can\'t be none!')

	def get_graph_layout(self, graph_id, layout_id=None, name=None, owner_email=None):
		"""Get a layout with given layout_id or name for the graph with given graph_id.

		:param graph_id: ID of the graph.
		:param layout_id: ID of the layout.
		:param name: Name of the layout.
		:return: LayoutResponse object that wraps the response.
		"""
		if layout_id is not None:
			layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
			return LayoutResponse(
				self.client._make_request("GET", layout_by_id_path)
			)

		if name is not None:
			query = {
				'owner_email': self.client.username if owner_email is None else owner_email,
				'name': name
			}
			if owner_email is not None and owner_email != self.client.username:
				query.update({'is_shared': 1})
			layouts_path = LAYOUTS_PATH.format(graph_id)
			response = self.client._make_request("GET", layouts_path, url_params=query)
			if response.get('total', 0) > 0:
				return LayoutResponse(
					response.get('layouts')[0]
				)
			else:
				return None

		raise Exception('Both layout_id and name can\'t be none!')

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
