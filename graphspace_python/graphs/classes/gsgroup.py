import datetime


class GSGroup(object):
	"""GSGroup Class

	"""

	def __init__(self, name=None, description=None):
		"""Construct a new 'GSGroup' object.

		:param name: Name of the group. Default value is None.
		:param description: Description of the group. Default value is None.
		"""
		if name is None:
			self.set_name('Group ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
		else:
			self.name = name
		if description is not None:
			self.description = description

	def json(self):
		"""
		Get the json representation of group details.

		:return: dict
		"""
		data = {
			'name': self.get_name(),
			'description': self.get_description()
		}
		return data

	def get_name(self):
		"""
		Get the name of group.

		:return: string
		"""
		return self.name

	def set_name(self, name):
		"""
		Set the name of the group.

		:param name: name of the group.
		"""
		self.name = name

	def get_description(self):
		"""
		Get description of the group.

		:return: string
		"""
		return self.description

	def set_description(self, description):
		"""
		Set description of the group.

		:param description: description of the group.
		"""
		self.description = description
