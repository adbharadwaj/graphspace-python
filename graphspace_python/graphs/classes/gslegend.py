import datetime


class GSLegend(object):
	"""GSLegend class.

	A GSLegend stores the details of legend.

	It holds the information about the legend such as legend label and style of legend keys.

	It provides methods to add, retrieve, modify and remove the detatils of the legend.

	Attributes:
		legend_json (dict): JSON representation of the legend data.
	"""
	def __init__(self, *args, **kwargs):
		"""Construct a new 'GSLegend' object.

		"""
		self.legend_json = {'legend': {}}

	def set_legend_json(self, legend_json):
		"""Set the json representation of the legend.

		Args:
			legend_json(dict): JSON representation of the legend data.

		Examples:
			>>> from graphspace_python.graphs.classes.gslegend import GSLegend
			>>> G = GSLegend()
			>>> legend_json = {
			...	    "legend":{
			...	        "nodes":{
			...	            "Source Receptor": {
			...	                "shape":"triangle",
			...	                "background-color":"#ff1400"
			...	             },
			...	            "Receptor": {
			...	                "shape":"circle",
			...	                "background-color":"#1900ff"
			...	            }
			...	        },
			...	        "edges":{
			...	            "Phosphorylation":{
			...	                "line-color":"#0fcf25",
			...	                "line-style":"solid",
			...	                "arrow-shape":"triangle"
			...	            }
			...	        }
			...	    }
			...	}
			>>> G.set_legend_json(legend_json)
			>>> G.get_legend_json()
			{'legend': {'edges': {'Phosphorylation': {'arrow-shape': 'triangle', 'line-color': '#0fcf25', 'line-style': 'solid'}},
			'nodes': {'Receptor': {'background-color': '#1900ff', 'shape': 'circle'},
			'Source Receptor': {'background-color': '#ff1400', 'shape': 'triangle'}}}}
		"""
		self.legend_json = legend_json

	def get_legend_json(self):
		"""Get the json representation of the legend.

		Returns:
			dict: JSON representation of legend data.

		Examples:
			>>> from graphspace_python.graphs.classes.gslegend import GSLegend
			>>> G = GSLegend()
			>>> G.get_legend_json()
			{'legend': {}}
			>>> G.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
			>>> G.get_legend_json()
			{'legend': {'nodes': {'Receptor': {'background-color': 'black',
			'shape': 'star'}}}}
		"""
		return self.legend_json

	def add_legend_entries(self, element_type, label, style):
		"""Add an individual legend key to the legend data.

		Args:
			element_type(str): Either nodes or edges.
			label(str): Label of legend key.Passing an already existing label as param will update that legend key.
			style(dict): Style dict of the legend key. Will contain attributes like node shape or edge type, color.

		Examples:
			>>> from graphspace_python.graphs.classes.gslegend import GSLegend
			>>> G = GSLegend()
			>>> G.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
			>>> G.get_legend_json()
			{'legend': {'nodes': {'Receptor': {'background-color': 'black',
			'shape': 'star'}}}}
		"""
		from graphspace_python.graphs.classes.gsgraph import GSGraph

		GSGraph.validate_style_properties(style, element_type)
		if(element_type == 'nodes'):
			GSLegend.validate_node_legend_properties(style)
		else:
			GSLegend.validate_edge_legend_properties(style)

		legend_dict = dict()
		legend_dict[label] = style

		legend_json = self.get_legend_json()
		if(element_type in legend_json['legend']):
			legend_json['legend'][element_type].update(legend_dict)
		else:
			legend_json['legend'].update({element_type: legend_dict})

		self.set_legend_json(legend_json)

	def remove_legend_entries(self, element_type, label):
		"""Remove an individual legend key from the legend data.

		Args:
			element_type(str): Either nodes or edges.
			label(str): Label of legend key to be deleted.

		Examples:
			>>> from graphspace_python.graphs.classes.gslegend import GSLegend
			>>> G = GSLegend()
			>>> G.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
			>>> G.get_legend_json()
			{'legend': {'nodes': {'Receptor': {'background-color': 'black',
			'shape': 'star'}}}}
			>>> G.remove_legend_entries('nodes', 'Receptor')
			>>> G.get_legend_json()
			{'legend': {}}
		"""
		legend_json = self.get_legend_json()
		if(label not in legend_json['legend'].get(element_type, {})):
			raise KeyError("No legend exist with this label. Please verify the legend to remove exists.")
		else:
			del legend_json['legend'][element_type][label]
			self.set_legend_json(legend_json)

	def delete_legend_json(self):
		"""Set legend_json to NULL.

		Examples:
			>>> from graphspace_python.graphs.classes.gslegend import GSLegend
			>>> G = GSLegend()
			>>> G.add_legend_entries(element_type='nodes', label='Receptor', style={'background-color': 'black', 'shape':'star'})
			>>> G.get_legend_json()
			{'legend': {'nodes': {'Receptor': {'background-color': 'black',
			'shape': 'star'}}}}
			>>> G.delete_legend_json()
			>>> G.get_legend_json()
			{'legend': {}}
		"""
		legend_json = {'legend':{}}
		self.set_legend_json(legend_json)

	@staticmethod
	def validate_node_legend_properties(data_properties):
		if "background-color" not in data_properties:
			raise KeyError("All node legend must have background-color property.  Please verify that the new node legend meet this requirement.")
		if "shape" not in data_properties:
			raise KeyError("All node legend must have shape property.  Please verify that the new node legend meet this requirement.")

	@staticmethod
	def validate_edge_legend_properties(data_properties):
		if "line-color" not in data_properties:
			raise KeyError("All edge legend must have line-color property.  Please verify that the new edge legend meet this requirement.")
		if "line-style" not in data_properties:
			raise KeyError("All edge legend must have line-style property.  Please verify that the new edge legend meet this requirement.")
		if "arrow-shape" not in data_properties:
			raise KeyError("All edge legend must have arrow-shape property.  Please verify that the new edge legend meet this requirement.")