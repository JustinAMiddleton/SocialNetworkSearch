'''

Created on Feb 18, 2015

@author: Randy

'''

from Tkinter import *
from Interface import Interface
import time
import threading
import thread
import sys
import Queue

class Attribute():
	name = "Attribute"
	words = None
	weights = None
	sentiments = None

	def set_words(self, words):
		self.words = words

	def set_weights(self, weights):
		newWeights = []
		for weight in weights:
			if weight == "High":
				newWeights.append(3)
			elif weight == "Medium":
				newWeights.append(2)
			else:
				newWeights.append(1)
		self.weights = newWeights

	def set_sentiments(self, sentiments):
		newSentiments = []
		for sentiment in sentiments:
			if sentiment == "Positive":
				newSentiments.append(1)
			else:
				newSentiments.append(-1)
		self.sentiments = newSentiments

	def get_word(self, index):
		return self.words[index]

	def get_weight(self, index):
		if self.weights[index] == 3:
			return "High"
		elif self.weights[index] == 2:
			return "Medium"
		else:
			return "Low"

	def get_sentiment(self, index):
		if self.sentiments[index] == 1:
			return "Positive"
		else:
			return "Negative"


class GuiThread(threading.Thread):
	def __init__(self, attributes, args):
		threading.Thread.__init__(self)
		self.interface = None
		self.words = attributes[0].words
		self.weights = attributes[0].weights
		self.sentiments = attributes[0].sentiments
		self.args = args
	def run(self):
		zip(self.words,self.weights,self.sentiments)
		self.interface = Interface(self.words, self.weights, self.sentiments)
		self.query = self.interface.get_query(self.words)
		self.interface.search(self.query, self.args)
		self.results = self.interface.score()
		time.sleep(1)
	def stop(self):
		self.interface.stop_search()

class ThreadSafeConsole(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.queue = Queue.Queue()
        self.update_me()
    def write(self, line):
        self.queue.put(line)
    def clear(self):
        self.queue.put(None)
    def update_me(self):
        try:
            while 1:
                line = self.queue.get_nowait()
                if line is None:
                    self.delete(1.0, END)
                else:
                    self.insert(END, str(line))
                self.see(END)
                self.update_idletasks()
        except Queue.Empty:
            pass
        self.after(100, self.update_me)

class App():
	attributes = []
	
	def __init__(self, master): 
		self.frame = Frame(master)
		self.frame.pack()
		self.frame.grid(pady=15, padx=15)
		master.title("Whistleblower Analysis")
		master.geometry('460x310-625+200')

		self.initialize_attributes()
		self.create_main_window_controls()
	

	def initialize_attributes(self):
		for i in range(0, 5): 
			self.attributes.append(Attribute())

	def search(self):
		args = {}

		if self.location.get() is not None:
			args['location'] = self.location.get()

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

	def create_output_window(self):
		toplevel= Toplevel()
		toplevel.title('Output')
		toplevel.focus_set()
		output_frame = Frame(toplevel)
		output_frame.pack()

		self.widget = ThreadSafeConsole(output_frame, height=5, width=50)
		self.widget.grid(column=0, row=5, columnspan=2)
		sys.stdout = self.widget

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

		var=StringVar(options)
		var.set("Select Date")
		datePicker = OptionMenu(options, var, "Last 30 Days",
				    "Last 90 Days", "Past Year")
		datePicker.grid(row=6, pady=10, padx=5, sticky=W)
		datePicker.config(state = DISABLED)
	
	def create_main_window_command_controls(self):
		buttons = Frame(self.frame)
		buttons.grid(row=8, column=0, rowspan=2, columnspan=4, pady=10)

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
