import base64
import requests
import six
import inspect
from future.standard_library import install_aliases
install_aliases()

from graphspace_python.api.config import API_HOST
from graphspace_python.api.endpoint.graphs import Graphs
from graphspace_python.api.endpoint.layouts import Layouts
from graphspace_python.api.endpoint.groups import Groups
from graphspace_python.api.errors import ErrorHandler

class GraphSpace(object):
	"""GraphSpace Client Class
	"""

	_endpoints = [
		Graphs,
		Layouts,
		Groups
	]

	def __init__(self, username, password):
		"""Construct a new 'GraphSpace' client object.

		:param username: Username of the user.
		:param password: Password of the user.
		"""
		# self.auth_token = 'Basic %s' % base64.b64encode('{0}:{1}'.format(username, password))
		self.auth_token = requests.auth.HTTPBasicAuth(username, password)
		self.username = username
		self.api_host = API_HOST
		self._error_handler = ErrorHandler()
		self._define_request_methods()

	def _define_request_methods(self):
		"""Creates an instance of each endpoint and adds the public methods of each
		instance to the GraphSpace Client. It promotes modularity.
		"""
		endpoint_instances = [end(self) for end in self._endpoints]
		for endpoint in endpoint_instances:
			instance_methods = inspect.getmembers(endpoint, inspect.ismethod)
			self._add_instance_methods(instance_methods)

	def _add_instance_methods(self, instance_methods):
		"""Adds the instance methods to GraphSpace client.

		:param instance_methods: List of (name, value) tuples where value is the
		 instance of the bound method.
		"""
		for method in instance_methods:
			if method[0][0] is not '_':
				self.__setattr__(method[0], method[1])

	def set_api_host(self, host):
		"""Manually set host address of GraphSpace REST APIs.

		:param host: String - Host address of GraphSpace APIs.
		"""
		self.api_host = host

	def _check_error(self, response):
		"""Checks if the response has any HTTPError and raise exception else
		returns the response json data.

		:param response: Response object from API call.
		:raises GraphSpaceError: Raises error according to the error code.
		:return: Response Dict.
		"""
		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as error:
			self._error_handler.raise_error(error, response.json())
		else:
			return response.json()

	def _make_request(self, method, path, url_params={}, data={}, headers=None):
		"""Calls the GraphSpace REST API in the given endpoint, in the given method,
		with the given data, url params and headers.

		:param method: String - Method of request.
		:param path: String - Path of request.
		:param url_params: Dict - URL parameters for request.
		:param data: Dict - Payload.
		:param headers: Dict - Headers for the request.

		:return: Response Dict.
		"""
		if headers is None:
			headers = {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			}

		if method == "GET":
			return self._check_error(
				requests.get('http://{0}{1}?{2}'.format(
					self.api_host,
					six.moves.urllib.parse.quote(path.encode('utf-8')),
					six.moves.urllib.parse.urlencode(url_params, doseq=True)
				), headers=headers, auth=self.auth_token)
			)
		elif method == "POST":
			if headers.get('Content-Type') == 'application/json':
				return self._check_error(
					requests.post('http://{0}{1}?{2}'.format(
						self.api_host,
						six.moves.urllib.parse.quote(path.encode('utf-8')),
						six.moves.urllib.parse.urlencode(url_params)
					), json=data, headers=headers, auth=self.auth_token)
				)
			else:
				return self._check_error(
					requests.post('http://{0}{1}?{2}'.format(
						self.api_host,
						six.moves.urllib.parse.quote(path.encode('utf-8')),
						six.moves.urllib.parse.urlencode(url_params)
					), data=data, headers=headers, auth=self.auth_token)
				)
		elif method == "PUT":
			if headers.get('Content-Type') == 'application/json':
				return self._check_error(
					requests.put('http://{0}{1}?{2}'.format(
						self.api_host,
						six.moves.urllib.parse.quote(path.encode('utf-8')),
						six.moves.urllib.parse.urlencode(url_params)
					), json=data, headers=headers, auth=self.auth_token)
				)
			else:
				return self._check_error(
					requests.put('http://{0}{1}?{2}'.format(
						self.api_host,
						six.moves.urllib.parse.quote(path.encode('utf-8')),
						six.moves.urllib.parse.urlencode(url_params)
					), data=data, headers=headers, auth=self.auth_token)
				)
		elif method == "DELETE":
			return self._check_error(
				requests.delete('http://{0}{1}?{2}'.format(
					self.api_host,
					six.moves.urllib.parse.quote(path.encode('utf-8')),
					six.moves.urllib.parse.urlencode(url_params)
				), headers=headers, auth=self.auth_token)
			)
