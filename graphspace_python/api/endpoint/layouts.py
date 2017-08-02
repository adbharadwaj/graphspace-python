from graphspace_python.api.config import LAYOUTS_PATH
from graphspace_python.api.obj.api_response import APIResponse

class Layouts(object):
	"""Layouts endpoint class.

	Provides methods for layout related operations such as saving, fetching, updating and deleting layouts on GraphSpace.
	"""

	def __init__(self, client):
		self.client = client

	def post_graph_layout(self, graph_id, layout):
		"""Create a layout for the graph with given graph_id.

		Args:
			graph_id (int): ID of the graph.
			layout (GSLayout or Layout): Object having layout details, such as name, is_shared, style_json, positions_json.

		Returns:
		 	Layout: Saved layout on GraphSpace.

		Raises:
			GraphSpaceError: If error response is received from the GraphSpace API.

		Example:
			>>> # Connecting to GraphSpace
			>>> from graphspace_python.api.client import GraphSpace
			>>> graphspace = GraphSpace('user1@example.com', 'user1')
			>>> # Creating a layout
			>>> from graphspace_python.graphs.classes.gslayout import GSLayout
			>>> L = GSLayout()
			>>> L.set_node_position('a', y=38.5, x=67.3)
			>>> L.add_node_style('a', shape='ellipse', color='green', width=60, height=60)
			>>> L.set_name('My Sample Layout')
			>>> L.set_is_shared(1)
			>>> # Saving layout on GraphSpace
			>>> graphspace.post_graph_layout(graph_id=65390, layout=L)

		Note:
			Refer to the `tutorial <../tutorial/tutorial.html#creating-a-layout>`_ for more about posting layouts.
		"""
		data = layout.json()
		data.update({'graph_id': graph_id, 'owner_email': self.client.username})
		layouts_path = LAYOUTS_PATH.format(graph_id)
		return APIResponse('layout',
			self.client._make_request("POST", layouts_path, data=data)
		).layout

	def update_graph_layout(self, graph_id, layout, name=None, layout_id=None, owner_email=None):
		"""Update a layout with given layout_id or name for the graph with given graph_id.

		Args:
			graph_id (int): ID of the graph.
			layout (GSLayout or Layout): Object having layout details, such as name, is_shared, style_json, positions_json.
			name (str, optional): Name of the layout to be updated. Defaults to None.
			layout_id (int, optional): ID of the layout to be updated. Defaults to None.
			owner_email (str, optional): Email of owner of layout. Defaults to None.

		Returns:
		 	Layout: Updated layout on GraphSpace.

		Raises:
			Exception: If both 'name' and 'layout_id' are None or if layout doesnot exist.
			GraphSpaceError: If error response is received from the GraphSpace API.

		Examples:
			Updating a layout by creating a new layout and replacing the existing layout:

			>>> # Connecting to GraphSpace
			>>> from graphspace_python.api.client import GraphSpace
			>>> graphspace = GraphSpace('user1@example.com', 'user1')
			>>> # Creating the new layout
			>>> L = GSLayout()
			>>> L.set_node_position('a', y=102, x=238.1)
			>>> L.add_node_style('a', shape='octagon', color='green', width=60, height=60)
			>>> L.set_name('My Sample Layout')
			>>> L.set_is_shared(1)
			>>> # Updating to replace the existing layout
			>>> graphspace.update_graph_layout(graph_id=65390, layout=L, name='My Sample Layout')

			Another way of updating a layout by fetching and editing the existing layout:

			>>> # Fetching the layout
			>>> layout = graphspace.get_graph_layout(name='My Sample Layout')
			>>> # Modifying the fetched layout
			>>> layout.set_node_position('a', y=30, x=211)
			>>> layout.add_node_style('a', shape='roundrectangle', color='green', width=45, height=45)
			>>> layout.set_is_shared(0)
			>>> # Updating layout
			>>> graphspace.update_graph_layout(graph_id=65390, layout=layout, name='My Sample Layout')

			You can update a layout by id as well:

			>>> graphspace.update_graph_layout(graph_id=65390, layout=L, layout_id=1087)

		Note:
			Refer to the `tutorial <../tutorial/tutorial.html#updating-a-layout-on-graphspace>`_ for more about updating layouts.
		"""
		if layout_id is not None:
			layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
			return APIResponse('layout',
				self.client._make_request("PUT", layout_by_id_path, data=layout.json())
			).layout

		if name is not None:
			layout1 = self.get_graph_layout(graph_id=graph_id, name=name, owner_email=owner_email)
			if layout1 is None or layout1.id is None:
				raise Exception('Layout with name `%s` of graph with graph_id=%s doesnt exist for user `%s`!' % (name, graph_id, self.client.username))
			else:
				layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout1.id)
				return APIResponse('layout',
					self.client._make_request("PUT", layout_by_id_path, data=layout.json())
				).layout

		raise Exception('Both layout_id and name can\'t be none!')

	def delete_graph_layout(self, graph_id, name=None, layout_id=None):
		"""Delete a layout with the given layout_id or name for the graph with given graph_id.

		Args:
			graph_id (int): ID of the graph.
			name (str, optional): Name of the layout to be deleted. Defaults to None.
			layout_id (int, optional): ID of the layout to be deleted. Defaults to None.

		Returns:
		 	str: Success/Error Message from GraphSpace.

		Raises:
			Exception: If both 'name' and 'layout_id' are None or if layout doesnot exist.
			GraphSpaceError: If error response is received from the GraphSpace API.

		Examples:
			Deleting a layout by name:

			>>> # Connecting to GraphSpace
			>>> from graphspace_python.api.client import GraphSpace
			>>> graphspace = GraphSpace('user1@example.com', 'user1')
			>>> # Deleting a layout
			>>> graphspace.delete_graph_layout(graph_id=65390, name='My Sample Layout')
			u'Successfully deleted layout with id=1087'

			Deleting a layout by id:

			>>> graphspace.delete_graph_layout(graph_id=65930, layout_id=1087)
			u'Successfully deleted layout with id=1087'

		Note:
			Refer to the `tutorial <../tutorial/tutorial.html#deleting-a-layout-on-graphspace>`_ for more about deleting layouts.
		"""
		if layout_id is not None:
			layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
			response = self.client._make_request("DELETE", layout_by_id_path)
			return response['message']

		if name is not None:
			layout = self.get_graph_layout(graph_id=graph_id, name=name)
			if layout is None or layout.id is None:
				raise Exception('Layout with name `%s` of graph with graph_id=%s doesnt exist for user `%s`!' % (name, graph_id, self.client.username))
			else:
				layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout.id)
				response = self.client._make_request("DELETE", layout_by_id_path)
				return response['message']

		raise Exception('Both layout_id and name can\'t be none!')

	def get_graph_layout(self, graph_id, name=None, layout_id=None, owner_email=None):
		"""Get a layout with given layout_id or name for the graph with given graph_id.

		Args:
			graph_id (int): ID of the graph.
			name (str, optional): Name of the layout to be fetched. Defaults to None.
			layout_id (int, optional): ID of the layout to be fetched. Defaults to None.
			owner_email (str, optional): Email of owner of layout. Defaults to None.

		Returns:
		 	Layout or None: Layout object, if layout with the given 'name' or 'layout_id' exists; otherwise None.

		Raises:
			Exception: If both 'name' and 'layout_id' are None.
			GraphSpaceError: If error response is received from the GraphSpace API.

		Examples:
			Getting a layout by name:

			>>> # Connecting to GraphSpace
			>>> from graphspace_python.api.client import GraphSpace
			>>> graphspace = GraphSpace('user1@example.com', 'user1')
			>>> # Fetching a layout
			>>> layout = graphspace.get_graph_layout(graph_id=65390, name='My Sample Layout')
			>>> layout.get_name()
			u'My Sample Layout'

			Getting a layout by id:

			>>> layout = graphspace.get_graph_layout(graph_id=65390, layout_id=1087)
			>>> layout.get_name()
			u'My Sample Layout'

		Note:
			Refer to the `tutorial <../tutorial/tutorial.html#fetching-a-layout-from-graphspace>`_ for more about fetching layouts.
		"""
		if layout_id is not None:
			layout_by_id_path = LAYOUTS_PATH.format(graph_id) + str(layout_id)
			return APIResponse('layout',
				self.client._make_request("GET", layout_by_id_path)
			).layout

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
				return APIResponse('layout',
					response.get('layouts')[0]
				).layout
			else:
				return None

		raise Exception('Both layout_id and name can\'t be none!')

	def get_my_graph_layouts(self, graph_id, limit=20, offset=0):
		"""Get layouts created by the requesting user for the graph with given graph_id.

		Args:
			graph_id (int): ID of the graph.
			offset (int, optional): Offset the list of returned entities by this number. Defaults to 0.
			limit (int, optional): Number of entities to return. Defaults to 20.

		Returns:
		 	List[Layout]: List of layouts owned by the requesting user.

		Raises:
			GraphSpaceError: If error response is received from the GraphSpace API.

		Example:
			>>> # Connecting to GraphSpace
			>>> from graphspace_python.api.client import GraphSpace
			>>> graphspace = GraphSpace('user1@example.com', 'user1')
			>>> # Fetching my graph layouts
			>>> layouts = graphspace.get_my_graph_layouts(graph_id=65390, limit=5)
			>>> layouts[0].get_name()
			u'My Sample Layout'
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'owner_email': self.client.username
		}

		layouts_path = LAYOUTS_PATH.format(graph_id)
		return APIResponse('layout',
			self.client._make_request("GET", layouts_path, url_params=query)
		).layouts

	def get_shared_graph_layouts(self, graph_id, limit=20, offset=0):
		"""Get layouts shared with the requesting user for the graph with given graph_id.

		Args:
			graph_id (int): ID of the graph.
			offset (int, optional): Offset the list of returned entities by this number. Defaults to 0.
			limit (int, optional): Number of entities to return. Defaults to 20.

		Returns:
		 	List[Layout]: List of layouts shared with the requesting user.

		Raises:
			GraphSpaceError: If error response is received from the GraphSpace API.

		Example:
			>>> # Connecting to GraphSpace
			>>> from graphspace_python.api.client import GraphSpace
			>>> graphspace = GraphSpace('user1@example.com', 'user1')
			>>> # Fetching shared graph layouts
			>>> layouts = graphspace.get_shared_graph_layouts(graph_id=65390, limit=5)
			>>> layouts[0].get_name()
			u'Test Layout'
		"""
		query = {
			'limit': limit,
			'offset': offset,
			'is_shared': 1
		}

		layouts_path = LAYOUTS_PATH.format(graph_id)
		return APIResponse('layout',
			self.client._make_request("GET", layouts_path, url_params=query)
		).layouts
