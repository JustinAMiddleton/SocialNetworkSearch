'''

Created on Feb 18, 2015

@author: Randy

'''

from Tkinter import *
from Interface import Interface
from Attribute import Attribute
from SearchPacket import SearchPacket
from GuiThread import GuiThread
from AttributeWindow import AttributeWindow
from ResultsWindow import ResultsWindow
import time
import threading
import thread
import sys
import Queue

class App():
	attributes = []
	
	def __init__(self, master): 
		self.frame = Frame(master)
		self.frame.pack()
		self.frame.grid(pady=15, padx=15)
		master.title("Whistleblower Analysis")
		master.geometry('500x370-625+200')

		self.initialize_attribute_objects()
		self.create_main_window_controls()

	def search(self):
		self.start_button.config(state = DISABLED)
		self.thread = GuiThread(self.attributes, self.get_search_arguments())
		self.thread.start()
		
		while self.thread.interface == None:
			time.sleep(1)

		self.interface = self.thread.interface
		self.stop_button.config(state = NORMAL)

	def stop(self):
		self.stop_button.config(state = DISABLED)

		if self.thread.isAlive():
			self.thread.stop()
			self.thread.join()
	
		self.show_results_window()
		self.start_button.config(state = NORMAL)

	def initialize_attribute_objects(self):
		for i in range(0, 5): 
			self.attributes.append(Attribute())

	def show_attribute_window(self, attribute, index):
		attr_window = AttributeWindow()
		attr_window.create_attribute_window(self.attributes, self.attribute_labels, index)

	def show_results_window(self):
		results_window = ResultsWindow(self.interface.db)
		results_window.create_results_window()	

	def clear_attribute(self, index):
		self.attributes[index] = Attribute()
		self.attribute_labels[index]['text'] = "Attribute " + str(index+1)

	def get_search_arguments(self):
		args = {}
		args['location'] = None
		args['until'] = None
		args['since'] = None

		if not self.location.get() == "":
			args['location'] = self.location.get()
		if not self.date_until.get() in ("","yyyy-mm-dd"):
			args['until'] = self.date_until.get()
		if not self.date_since.get() in ("","yyyy-mm-dd"):
			print self.date_since.get()	
			args['since'] = self.date_since.get()

		return args

	def create_main_window_controls(self):
		self.create_main_window_attribute_controls()
		self.create_main_window_options_controls()
		self.create_main_window_command_controls()

	def create_main_window_attribute_controls(self):
		self.defAtt = "Define Attribute"
		attributes = Frame(self.frame)
		attributes.grid(row=0, column=0, rowspan=3, columnspan=3, padx=10, sticky=N)

		Label(attributes, text="Attributes", font = "Verdana 10 bold").grid(row=0, column=0, pady=4)

		self.create_attribute_label_controls(attributes)
		self.create_attribute_button_controls(attributes)
	
	def create_main_window_command_controls(self):
		buttons = Frame(self.frame)
		buttons.grid(row=8, column=0, rowspan=2, columnspan=4, pady=20)

		self.start_button = Button(buttons, text="Search", 
				command=self.search, font = "Verdana 10")
		self.start_button.grid(row=8)
		
		self.stop_button = Button(buttons, text="Stop", 
				command=self.stop, font = "Verdana 10")
		self.stop_button.grid(row=9, pady=5)
		self.stop_button.config(state = DISABLED)

	def create_attribute_label_controls(self, frame):
		self.attribute_labels = []
		for i in range(1, len(self.attributes)+1):
			attr_label = Label(frame, text="Attribute "+str(i), width=10, anchor=W)
			attr_label.grid(row=i, column=0, sticky=W, padx=10)	
			self.attribute_labels.append(attr_label)
	
	def create_attribute_button_controls(self, frame):
		for i in range(0, 5):
			Button(frame, text=self.defAtt, command=lambda i=i: self.show_attribute_window(self.attributes[i], i)).grid(
				    row=i+1, column=1, pady=4)
			Button(frame, text="X", command=lambda i=i: self.clear_attribute(i)).grid(row=i+1, column=2, padx=5)

	def create_main_window_options_controls(self):
		options = Frame(self.frame)
		options.grid(row=1, column=3, rowspan=7, columnspan=1, padx=10, sticky=S)

		Label(options, text="Options", font = "Verdana 10 bold").grid(row=0, pady=5, sticky=W)
		Label(options, text="Web Sites").grid(row=1, pady=5, sticky=W)

		twitter_enabled = IntVar()
		Checkbutton(options, text="Twitter", variable=twitter_enabled).grid(row=2,
				    sticky=W, padx=15)

		google_enabled = IntVar()
		googleCheck = Checkbutton(options, text="Google+", variable=google_enabled)
		googleCheck.config(state = DISABLED)
		googleCheck.grid(row=3, sticky=W, padx=15)

		Label(options, text="Location").grid(row=4, sticky=W, pady=5, padx=5)
		self.location = Entry(options, width=15)
		self.location.grid(row=5, padx=15)

		Label(options, text="Since Date").grid(row=6, sticky=W, pady=5, padx=5)
		self.date_since = Entry(options, width=15)
		self.date_since.insert(0, "yyyy-mm-dd")
		self.date_since.grid(row=7, padx=15)

		Label(options, text="Until Date").grid(row=8, sticky=W, pady=5, padx=5)
		self.date_until = Entry(options, width=15)
		self.date_until.insert(0, "yyyy-mm-dd")
		self.date_until.grid(row=9, padx=15)


root=Tk()
app = App(root)
root.mainloop()
