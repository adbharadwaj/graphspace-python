import datetime
from graphspace_python.graphs.classes.gsgraph import GSGraph


class GSLayout(object):
	"""GSLayout Class

	"""

	def __init__(self):
		self.style_json = {'style': []}
		self.positions_json = {}
		self.set_name('Layout ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

	def get_name(self):
		"""
		Get the name of layout.

		:return: string
		"""
		return self.name

	def set_name(self, name):
		"""
		Set the name of the layout.

		:param name: name of the layout.
		"""
		self.name = name

	def get_positions_json(self):
		"""
		Get the json representation for the layout node postitions.

		:return: dict
		"""
		return self.positions_json

	def set_positions_json(self, positions_json):
		"""
		Set the json representation for the layout node postitions.

		:param positions_json: dict - json representation for the node positions
		"""
		self.positions_json = positions_json

	def get_node_position(self, node_name):
		"""
		Get the position of a node.

		:param node_name: name of the node.
		:return: Dict of x,y co-ordinates of the node.
		"""
		return self.positions_json.get(node_name, None)

	def set_node_position(self, node_name, y, x):
		"""
		Sets the position of a node.

		:param node_name: name of the node.
		:param y: y co-ordinate of node.
		:param x: x co-ordinate of node.
		"""
		node_position = {
			node_name: {
				'y': y,
				'x': x
			}
		}
		self.positions_json.update(node_position)

	def remove_node_position(self, node_name):
		"""
		Remove the position of a node.

		:param node_name: name of the node.
		"""
		if node_name not in self.positions_json.keys():
			raise Exception("Positions of node '%s' is undefined." % (node_name))
		else:
			del self.positions_json[node_name]

	def get_style_json(self):
		"""
		Get the json representation for the layout style.

		:return: dict
		"""
		return self.style_json

	def set_style_json(self, style_json):
		"""
		Set the json representation for the layout style.

		:param style_json: dict - json representation for the layout structure
		"""
		GSGraph.validate_style_json(style_json)
		self.style_json = style_json

	def add_node_style(self, node_name, attr_dict=None, content=None, shape='ellipse', color='#FFFFFF', height=None,
	                                   width=None, bubble=None, valign='center', halign='center', style="solid",
	                                   border_color='#000000', border_width=1):
		"""
		Add the style for the given node in the style json.

		Parameters
		----------
		node_name: string - name of the node.
		shape: string -- shape of node. Default = "ellipse".
		color: string -- hexadecimal representation of the color (e.g., #FFFFFF) or color name. Default = white.
		height: int -- height of the node's body. Use None to determine height from the number of lines in the label. Default = None.
		width: int -- width of the node's body, or None to determine width from length of label.  Default=None.
		bubble: string -- color of the text outline. Using this option gives a "bubble" effect; see the bubbleeffect() function. Optional.
		valign: string -- vertical alignment. Default = center.
		halign: string -- horizontal alignment. Default = center.
		style: string -- style of border. Default is "solid".  If Bubble is specified, then style is overwritten.
		border_color: string -- color of border. Default is #000000. If Bubble is specified, then style is overwritten.
		border_width: int -- width of border. Default is 4.  If Bubble is specified, then style is overwritten.


		Returns
		-------
		None

		"""
		attr_dict = attr_dict if attr_dict is not None else dict()

		selector = 'node[name="%s"]' % node_name

		style_properties = {}
		style_properties = GSGraph.set_node_shape_property(style_properties, shape)
		style_properties = GSGraph.set_node_color_property(style_properties, color)
		style_properties = GSGraph.set_node_label_property(style_properties, content)
		style_properties = GSGraph.set_node_width_property(style_properties, width)
		style_properties = GSGraph.set_node_height_property(style_properties, height)
		style_properties = GSGraph.set_node_vertical_alignment_property(style_properties, valign)
		style_properties = GSGraph.set_node_horizontal_alignment_property(style_properties, halign)
		style_properties = GSGraph.set_node_border_style_property(style_properties, style)
		style_properties = GSGraph.set_node_border_color_property(style_properties, border_color)
		style_properties = GSGraph.set_node_border_width_property(style_properties, border_width)

		# If bubble is specified, use the provided color,
		if bubble:
			style_properties = GSGraph.set_node_bubble_effect_property(style_properties, bubble, whitetext=False)

		attr_dict.update(style_properties)

		self.set_style_json({
			'style': self.get_style_json().get('style') + [{
				'selector': selector,
				'style': attr_dict
			}]
		})

	def add_edge_style(self, source, target, attr_dict=None, directed=False, color='#000000', width=1.0, arrow_shape='triangle',
	                   edge_style='solid', arrow_fill='filled'):
		"""Add the style for the given edge in the style json.

		source: string -- unique ID of the source node
		target: string -- unique ID of the target node
		color: string -- hexadecimal representation of the color (e.g., #000000), or the color name. Default = black.
		directed: bool - if True, draw the edge as directed. Default = False.
		width: float -- width of the edge.  Default = 1.0
		arrow_shape: string -- shape of arrow head. Default is "triangle"
		edge_style: string -- style of edge. Default is "solid"
		arrow_fill: string -- fill of arrow. Default is "filled"

		Returns
		-------
		None

		"""
		data_properties = {}
		style_properties = {}
		data_properties.update({"source": source, "target": target})
		style_properties = GSGraph.set_edge_color_property(style_properties, color)
		style_properties = GSGraph.set_edge_width_property(style_properties, width)
		style_properties = GSGraph.set_edge_target_arrow_shape_property(style_properties, arrow_shape)
		style_properties = GSGraph.set_edge_directionality_property(style_properties, directed, arrow_shape)
		style_properties = GSGraph.set_edge_line_style_property(style_properties, edge_style)
		style_properties = GSGraph.set_edge_target_arrow_fill(style_properties, arrow_fill)

		attr_dict = attr_dict if attr_dict is not None else dict()

		selector = 'edge[source="%s"][target="%s"]' % (source, target)

		attr_dict.update(style_properties)

		self.set_style_json({
			'style': self.get_style_json().get('style') + [{
				'selector': selector,
				'style': attr_dict
			}]
		})
