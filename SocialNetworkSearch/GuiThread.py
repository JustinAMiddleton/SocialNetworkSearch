import threading
import time
from Interface import Interface
from SearchPacket import SearchPacket

'''
This class controls the backend of the Whistleblower tools.
The GUI creates a multithreading environment to allow operations
via the backend to be controlled by the GUI.

Takes in a list of Attribute objects and a dictionary of
search arguments.

@author: Brenden Romanowski
@date: 17 March 2015
'''

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
		self.interface.score()
		time.sleep(1)
	def stop(self):
		self.interface.stop_search()
