import threading
import time
from Interface import Interface
from SearchPacket import SearchPacket

class GuiThread(threading.Thread):
	def __init__(self, attributes, args):
		threading.Thread.__init__(self)
		self.interface = None
		self.search_packet = SearchPacket(attributes)
		self.args = args
	def run(self):
		self.interface = Interface(self.search_packet)
		self.query = self.search_packet.getQuery()
		self.interface.search(self.query, self.args)
		self.results = self.interface.score()
		time.sleep(1)
	def stop(self):
		self.interface.stop_search()
