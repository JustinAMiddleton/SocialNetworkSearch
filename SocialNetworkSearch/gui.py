'''

Created on Feb 18, 2015

@author: Randy

'''

from Tkinter import *
from Interface import Interface
from Attribute import Attribute
from SearchPacket import SearchPacket
import time
import threading
import thread
import sys
import Queue

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

class App():
	attributes = []
	
	def __init__(self, master): 
		self.frame = Frame(master)
		self.frame.pack()
		self.frame.grid(pady=15, padx=15)
		master.title("Whistleblower Analysis")
		master.geometry('460x370-625+200')

		self.initialize_attributes()
		self.create_main_window_controls()
	

	def initialize_attributes(self):
		for i in range(0, 5): 
			self.attributes.append(Attribute())

	def search(self):
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

		self.start_button.config(state = DISABLED)

		self.thread = GuiThread(self.attributes, args)
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
		self.interface.db.close()

		self.start_button.config(state = NORMAL)

	def create_main_window_controls(self):
		self.create_main_window_attribute_controls()
		self.create_main_window_options_controls()
		self.create_main_window_command_controls()
	
	def show_results_window(self):
		toplevel= Toplevel()
		toplevel.title('Results')
		toplevel.focus_set()
		toplevel.geometry('200x200-160+200')
		results_frame = Frame(toplevel)
		results_frame.pack()

		top_users = self.thread.results
		for i in range(0,len(top_users)):
			user = Label(results_frame, text="[%s] %s" % (str(round(top_users[i]['score'],1)), top_users[i]['username']))
			user.grid(row=i, column=0, sticky=W)	

	def define_attribute(self, attribute):
		self.toplevel= Toplevel()
		self.toplevel.title('Define Attribute')
		self.toplevel.focus_set()
		self.toplevel.geometry('450x230-160+200')
		self.attribute_frame = Frame(self.toplevel)
		self.attribute_frame.pack()

		values = self.create_attribute_controls(attribute)

		set_attribute = lambda: self.set_attribute_values(attribute, values)

		Button(self.attribute_frame, text="Save", command=set_attribute).grid(row=6, column=0,pady=10, padx=5)			

	def clear_attribute(self, index):
		self.attributes[index] = Attribute()

	def create_attribute_controls(self, attribute):	
		wordBoxes = []
		weightBoxes = []
		sentimentBoxes = []

		new_attribute = True
		if attribute.words is not None:
			new_attribute = False

		Label(self.attribute_frame, text="Name").grid(row=0, column=0, pady=5)
		nameBox = Entry(self.attribute_frame)
		nameBox.grid(row=0, column=1, pady=5)
		nameBox.insert(0, attribute.name)

		for i in range(1,6):
			Label(self.attribute_frame, text="Word "+str(i)).grid(row=i, column=0)
			wordBox = Entry(self.attribute_frame)
			wordBox.grid(row=i, column=1)

			weightStr = StringVar(self.toplevel)
			sentimentStr = StringVar(self.toplevel)
	
			weightBox = OptionMenu(self.attribute_frame, weightStr, "High", "Medium", "Low")
			sentimentBox = OptionMenu(self.attribute_frame, sentimentStr, "Positive", "Negative")

			weightBox.config(width=7)
			sentimentBox.config(width=7)
			weightBox.grid(row=i, column=2)
			sentimentBox.grid(row=i, column=3)

			if new_attribute:
				weightStr.set("Weight")
				sentimentStr.set("Positive")
			else:
				wordBox.insert(0, attribute.get_word(i-1))
				weightStr.set(attribute.get_weight(i-1))
				sentimentStr.set(attribute.get_sentiment(i-1))

			wordBoxes.append(wordBox)
			weightBoxes.append(weightStr)
			sentimentBoxes.append(sentimentStr)

		return [wordBoxes, weightBoxes, sentimentBoxes, nameBox]
	
	def set_attribute_values(self, attribute, values):
		words = self.get_control_values(values[0])
		weights = self.get_control_values(values[1])
		sentiments = self.get_control_values(values[2])
	
		attribute.name = values[3].get()
		attribute.set_words(words)
		attribute.set_weights(weights)
		attribute.set_sentiments(sentiments)

	def get_control_values(self, controls):
		values = []
		for control in controls:
			value = control.get()
			values.append(value)
		return values

	def create_main_window_attribute_controls(self):
		self.defAtt = "Define Attribute"
		attributes = Frame(self.frame)
		attributes.grid(row=0, column=0, rowspan=3, columnspan=3, padx=10, sticky=N)

		Label(attributes, text="Attributes", font = "Verdana 10 bold").grid(row=0, column=0, pady=4)

		self.create_attribute_label_controls(attributes)
		self.create_attribute_button_controls(attributes)

	def create_main_window_options_controls(self):
		options = Frame(self.frame)
		options.grid(row=1, column=3, rowspan=7, columnspan=1, padx=10, sticky=S)

		Label(options, text="Options", font = "Verdana 10 bold").grid(row=0, pady=5, sticky=W)
		Label(options, text="Web Sites").grid(row=1, pady=5, sticky=W)
		var1 = IntVar()
		Checkbutton(options, text="Twitter", variable=var1).grid(row=2,
				    sticky=W, padx=15)
		var2 = IntVar()
		googleCheck = Checkbutton(options, text="Google+", variable=var2)
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

		'''self.date_until=StringVar(options)
		self.date_until.set("Select Date")
		datePicker = OptionMenu(options, self.date_until, "Last 30 Days",
				    "Last 90 Days", "Past Year")
		datePicker.grid(row=6, pady=10, padx=5, sticky=W)
		#datePicker.config(state = DISABLED)'''
	
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
			attr_label = Label(frame, text="Attribute "+str(i))
			attr_label.grid(row=i, column=0)	
			self.attribute_labels.append(attr_label)
	
	def create_attribute_button_controls(self, frame):
		Button(frame, text=self.defAtt, command=lambda: self.define_attribute(self.attributes[0])).grid(
				    row=1, column=1, pady=4)
		Button(frame, text="X", command=lambda: self.clear_attribute(0)).grid(row=1, column=2, padx=5)

		Button(frame, text=self.defAtt, command=lambda: self.define_attribute(self.attributes[1])).grid(
				    row=2, column=1, pady=4)
		Button(frame, text="X", command=lambda: self.clear_attribute(1)).grid(row=2, column=2, padx=5)

		Button(frame, text=self.defAtt, command=lambda: self.define_attribute(self.attributes[2])).grid(
				    row=3, column=1, pady=4)
		Button(frame, text="X", command=lambda: self.clear_attribute(2)).grid(row=3, column=2, padx=5)

		Button(frame, text=self.defAtt, command=lambda: self.define_attribute(self.attributes[3])).grid(
				    row=4, column=1, pady=4)
		Button(frame, text="X", command=lambda: self.clear_attribute(3)).grid(row=4, column=2, padx=5)

		Button(frame, text=self.defAtt, command=lambda: self.define_attribute(self.attributes[4])).grid(
				    row=5, column=1, pady=4)
		Button(frame, text="X", command=lambda: self.clear_attribute(4)).grid(row=5, column=2, padx=5)


root=Tk()
app = App(root)
root.mainloop()
