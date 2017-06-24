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

	_endpoints = [
		Graphs,
		Layouts,
		Groups
	]

	def __init__(self, username, password):
		# self.auth_token = 'Basic %s' % base64.b64encode('{0}:{1}'.format(username, password))
		self.auth_token = requests.auth.HTTPBasicAuth(username, password)
		self.username = username
		self.api_host = API_HOST
		self._error_handler = ErrorHandler()
		self._define_request_methods()

	# Creates an instance of each endpoint and adds the public methods of each
	# instance to the GraphSpace Client. It promotes modularity.
	def _define_request_methods(self):
		endpoint_instances = [end(self) for end in self._endpoints]
		for endpoint in endpoint_instances:
			instance_methods = inspect.getmembers(endpoint, inspect.ismethod)
			self._add_instance_methods(instance_methods)

	def _add_instance_methods(self, instance_methods):
        # instance_methods is a list of (name, value) tuples where value is the
        # instance of the bound method
		for method in instance_methods:
			if method[0][0] is not '_':
				self.__setattr__(method[0], method[1])

	def set_api_host(self, host):
		self.api_host = host

	def _check_error(self, response):
		# Check if the response has any HTTPError and raise exception
		# else return the response json data
		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError as error:
			self._error_handler.raise_error(error, response.json())
		else:
			return response.json()

	def _make_request(self, method, path, url_params={}, data={}, headers=None):
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
			return self._check_error(
				requests.post('http://{0}{1}?{2}'.format(
					self.api_host,
					six.moves.urllib.parse.quote(path.encode('utf-8')),
					six.moves.urllib.parse.urlencode(url_params)
				), json=data, headers=headers, auth=self.auth_token)
			)
		elif method == "PUT":
			return self._check_error(
				requests.put('http://{0}{1}?{2}'.format(
					self.api_host,
					six.moves.urllib.parse.quote(path.encode('utf-8')),
					six.moves.urllib.parse.urlencode(url_params)
				), json=data, headers=headers, auth=self.auth_token)
			)
		elif method == "DELETE":
			return self._check_error(
				requests.delete('http://{0}{1}?{2}'.format(
					self.api_host,
					six.moves.urllib.parse.quote(path.encode('utf-8')),
					six.moves.urllib.parse.urlencode(url_params)
				), headers=headers, auth=self.auth_token)
			)
