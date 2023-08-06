import inspect
from .. import connector
from . import models


custom_dunders = {'__new__', '__init__', '__getattribute__', '__setattr__', '__call__', '__iter__', '__class__'}


class RemoteObject:

	# The three-underscore (tunder?) methods and variables:
	#
	# Their purpose is to be seperated from a method on the actual remote object.
	# When an attribute is called, and it's surrounded by '___', it gets called on this object,
	# instead of being sent to the server.

	def __init__(self, id: int, connection):
		self.___id___ = id
		self.___connection___: connector.Connection = connection

	def ___call_server___(self, method: str, function: str, data=None, **params):
		json = self.___connection___.call_server(method, function, data, id=self.___id___, **params)
		if isinstance(json, dict):
			return models.parse(json, self.___connection___)
		elif isinstance(json, list):
			return [models.parse(i, self.___connection___) for i in json]


	def __getattribute__(self, name: str, force_remote=False):
		def get_from_server():
			return self.___call_server___('get', 'getattr', attribute=name)
		if force_remote:
			return get_from_server()
		elif (name.startswith('___') and name.endswith('___')) or (name in custom_dunders):
			return super().__getattribute__(name)
		else:
			return get_from_server()


	def __setattr__(self, key, value, force_local=False):
		if force_local or (key.startswith('___') and key.endswith('___')):
			super().__setattr__(key, value)
		else:
			self.___call_server___('post', 'setattr', attribute=key, data=models.generate(value).dict())


	def __call__(self, *args, **kwargs):
		args = [models.generate(a) for a in args]
		kwargs = {key: models.generate(a) for (key, a) in kwargs.items()}
		return self.___call_server___('post', 'call', data=models.CallParameters(args=args, kwargs=kwargs).dict())


	def __iter__(self):
		list = self.___call_server___('get', 'iterate')
		return list.__iter__()


	@property
	def __class__(self):
		"""If possible, return local reference to class if the package that provides it is imported,
		otherwise return a RemoteObject as usual"""
		caller = inspect.stack()[2].frame
		remote_class = self.__getattribute__('__class__', force_remote=True)
		try:
			module = remote_class.__module__
			classname = remote_class.__qualname__
			if module not in {'builtins', '__builtin__'}:
				classname = module + '.' + classname
			return eval(classname, caller.f_globals, caller.f_locals)
		except:
			return remote_class





magic_methods = {
	'abs', 'add', 'and', 'bool', 'ceil', 'cmp', 'complex', 'contains', 'divmod', 'eq', 'float', 'floor', 'floordiv',
	'format', 'ge', 'getitem', 'getslice', 'gt', 'hash', 'index', 'int', 'invert', 'iter', 'le', 'len', 'lshift',
	'lt', 'matmul', 'mod', 'mul', 'ne', 'neg', 'next', 'nonzero', 'or', 'pos', 'pow', 'radd', 'rand', 'rdiv',
	'rdivmod', 'reversed', 'rfloordiv', 'rlshift', 'rmatmul', 'rmod', 'rmul', 'ror', 'round', 'rpow', 'rrshift',
	'rshift', 'rsub', 'rtruediv', 'rxor', 'sub', 'truediv', 'trunc', 'xor', 'delattr', 'delitem', 'delslice',
	'enter', 'exit', 'iadd', 'iand', 'ifloordiv', 'ilshift', 'imatmul', 'imod', 'imul', 'ior', 'ipow', 'irshift',
	'isub', 'itruediv', 'ixor', 'missing', 'setattr', 'setitem', 'setslice'
}


def make_function(dunder):
	def function(self, *args, **kwargs):
		return getattr(self, dunder)(*args, **kwargs)
	return function


for magic_method in magic_methods:
	magic_method = f'__{magic_method}__'
	if magic_method not in custom_dunders:
		setattr(RemoteObject, magic_method, make_function(magic_method))
