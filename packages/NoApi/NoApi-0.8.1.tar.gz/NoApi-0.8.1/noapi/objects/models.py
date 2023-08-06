import pydantic, typing, types
from . import local, remote



basic_types = {str, int, float, bool, None, types.NoneType}
"""Basic immutable types that can be sent as-is over the network"""



class LocalObjectInfo(pydantic.BaseModel):

	id: int
	basic: bool
	value: typing.Any

	@classmethod
	def generate(cls, object):
		object_id = id(object)
		basic = (type(object) in basic_types)

		local.requested[object_id] = object

		return cls(
			id=object_id,
			basic=basic,
			value=object if basic else None
		)

	def parse(self, connection):
		if self.basic:
			return self.value
		else:
			return remote.RemoteObject(self.id, connection)



class RemoteObjectInfo(pydantic.BaseModel):

	id: int

	@classmethod
	def generate(cls, object: remote.RemoteObject):
		return cls(id=object.___id___)

	def parse(self, connection=None):
		return local.requested[self.id]




def generate(object):
	if isinstance(object, remote.RemoteObject):
		return RemoteObjectInfo.generate(object)
	else:
		return LocalObjectInfo.generate(object)


def parse(json: dict, connection):
	if 'value' in json.keys():
		info = LocalObjectInfo(**json)
	else:
		info = RemoteObjectInfo(**json)
	return info.parse(connection)







class CallParameters(pydantic.BaseModel):

	args: list[LocalObjectInfo | RemoteObjectInfo]
	kwargs: dict[str, LocalObjectInfo | RemoteObjectInfo]

	def use_on(self, object, connection):
		args = [a.parse(connection) for a in self.args]
		kwargs = {key: arg.parse(connection) for (key, arg) in self.kwargs.items()}
		return object(*args, **kwargs)
