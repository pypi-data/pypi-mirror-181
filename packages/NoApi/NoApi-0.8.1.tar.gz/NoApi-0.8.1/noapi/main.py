import threading

from . import connector, objects


class Node:
	"""
	Activate to open the Python namespace for remote control of objects and variables.
	Without port forwarding works only on internal network, which is probably for the best. \n
	NOTE: Currently not secure in the slightest -
	anyone on the same network can access it just by knowing the port.

	:param port: any unique port for your program
	:param namespace: The starting point from the client's POV.
					  Tip: you can use __import__(__name__) if you want the current module.
	"""
	def __init__(self, port: int, namespace, activate_automatically=True, log=False):
		self.server = connector.Server(port, log)
		objects.local.generate_functions(self.server.fastapi, namespace, self.server.connections)
		if activate_automatically:
			self.activate()

	def activate(self):
		self.server.start()

	def deactivate(self):
		self.server.stop()


class Remote:
	"""
	Connect and use another device's objects
	"""
	def __init__(self, port: int, address: str, local_node: Node, connect_automatically=True):
		self.local_node = local_node
		self.connection = connector.Connection(address, port, self.local_node.server.port)
		self.control_portal: objects.remote.RemoteObject | None = None
		if connect_automatically:
			self.connect()

	def connect(self):
		self.connection.connect()
		root_info = self.connection.call_server('get', 'root')
		self.control_portal = objects.models.parse(root_info, self.connection)
