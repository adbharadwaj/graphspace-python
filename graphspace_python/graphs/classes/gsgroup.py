import datetime


class GSGroup(object):
	"""GSGroup class.

	Encapsulates details of a GraphSpace group and provides methods to read and manipulate the details.

	Attributes:
		name (str): Name of group.
		description (str): Description of group.
	"""

	def __init__(self, name=None, description=None):
		"""Construct a new 'GSGroup' object.

		Args:
			name (str, optional): Name of the group. Defaults to None.
			description (str, optional): Description of the group. Defaults to None.
		"""
		if name is None:
			self.set_name('Group ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
		else:
			self.name = name
		if description is not None:
			self.description = description

	def json(self):
		"""Get the json representation of group details.

		Returns:
			dict: Json representation of group details.
		"""
		data = {
			'name': self.get_name(),
			'description': self.get_description()
		}
		return data

	def get_name(self):
		"""Get the name of group.

		Returns:
			str: Name of group.
		"""
		return self.name

	def set_name(self, name):
		"""Set the name of the group.

		Args:
			name (str): Name of group.
		"""
		self.name = name

	def get_description(self):
		"""Get description of the group.

		Returns:
			str: Description of group.
		"""
		return self.description

	def set_description(self, description):
		"""Set description of the group.

		Args:
			description (str): Description of group.
		"""
		self.description = description
