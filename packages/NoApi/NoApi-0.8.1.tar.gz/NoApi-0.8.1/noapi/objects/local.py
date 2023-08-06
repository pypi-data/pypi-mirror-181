import typing, fastapi

from .. import connector
from . import models

requested: dict[int, typing.Any] = {}
"""Previously requested objects, from where they can be (re-)retrieved by id"""


def get_object(id: int):
	try:
		return requested[id]
	except KeyError as e:
		raise fastapi.HTTPException(404, str(e))





def generate_functions(fastapi_server: fastapi.FastAPI, namespace, connections: set[connector.Connection]):
	def _get_connection(request: fastapi.Request):
		address = request.client.host
		for connection in connections:
			if connection.short_address == address:
				return connection
		raise fastapi.HTTPException(403, "Client hasn't established connection")

	@fastapi_server.get('/root')
	def root():
		"""Get the id of the root object"""
		return models.LocalObjectInfo.generate(namespace)

	@fastapi_server.get('/getattr')
	def get_object_attr(id: int, attribute: str):
		try:
			object = getattr(get_object(id), attribute)
		except AttributeError as e:
			raise fastapi.HTTPException(404, str(e))
		return models.LocalObjectInfo.generate(object)

	@fastapi_server.post('/setattr')
	def set_object_attr(id: int, attribute: str, value: models.LocalObjectInfo | models.RemoteObjectInfo,
						request: fastapi.Request):
		setattr(get_object(id), attribute, value.parse(_get_connection(request)))

	@fastapi_server.get('/iterate')
	def iterate_object(id: int):
		object = get_object(id)
		return [models.LocalObjectInfo.generate(i) for i in object]

	@fastapi_server.post('/call')
	def call_object(id: int, params: models.CallParameters, request: fastapi.Request):
		object = get_object(id)
		result = params.use_on(object, _get_connection(request))
		return models.LocalObjectInfo.generate(result)
