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

class GuiThread(threading.Thread):
	def __init__(self, words, weights, sentiments, args):
		threading.Thread.__init__(self)
		self.words = words
		self.weights = weights
		self.sentiments = sentiments
		self.args = args
	def run(self):
		zip(self.words,self.weights,self.sentiments)
		self.interface = Interface(self.words, self.weights, self.sentiments)
		self.query = self.interface.get_query(self.words)
		self.interface.search(self.query, self.args)
		self.interface.score()
		self.interface.db.close()
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
	attribute1 = "Attribute 1"
	defAtt = "Define Attribute"

	attribute1_values = [["","High","Positive"],
				["","High","Positive"],
				["","High","Positive"],
				["","High","Positive"]]
	words = []
	weights = []
	sentiments = []
	
	def __init__(self, master): 
		self.frame = Frame(master)
		self.frame.pack()
		master.title("Whistleblower Analysis")

		self.create_output_window()
		self.create_main_window_controls()

	def search(self):
		args = {}

		if self.location.get() is not None:
			args['location'] = self.location.get()

		self.thread = GuiThread(self.words, self.weights, self.sentiments, args)
		self.thread.start()

	def stop(self):
		self.thread.stop()		

	def create_main_window_controls(self):
		Label(self.frame, text="Attribute").grid(row=0, column=0, sticky=E)
		Button(self.frame, text=self.defAtt, 
			command=self.create_attribute_window).grid(row=0, column=1,sticky=W+N)

		Label(self.frame, text="Location").grid(row=1, column=0)
		self.location = Entry(self.frame, width=15)
		self.location.grid(row=1, column=1)

		Button(self.frame, text="Search", 
			command=self.search).grid(row=4, column=0, 
						columnspan=2, sticky=W+E+S, pady=30)
		Button(self.frame, text="Stop", 
			command=self.stop).grid(row=4, column=0,
						columnspan=2, sticky=W+E+S)

	def create_output_window(self):
		toplevel= Toplevel()
		toplevel.title('Output')
		toplevel.focus_set()
		output_frame = Frame(toplevel)
		output_frame.pack()

		self.widget = ThreadSafeConsole(output_frame, height=30, width=50)
		self.widget.grid(column=0, row=5, columnspan=2)
		sys.stdout = self.widget

	def create_attribute_window(self): 
		toplevel= Toplevel()
		toplevel.title('Define Attribute')
		toplevel.focus_set()
		self.attribute_frame = Frame(toplevel)
		self.attribute_frame.pack()

		wordBoxes = []
		weights = []
		sentiments = []
		for i in range(0,4):
			Label(self.attribute_frame, text="Word "+str(i+1)).grid(row=i, column=0)
			wordBox = Entry(self.attribute_frame)
			wordBox.insert(0, self.attribute1_values[i][0])
			wordBox.grid(row=i, column=1)
			wordBoxes.append(wordBox)
			
			var1 = StringVar(toplevel)
			var1.set("Weight")
			if (self.attribute1_values[i][1] != ""):
				var1.set(self.attribute1_values[i][1])
			weight = OptionMenu(self.attribute_frame, var1, "High", "Medium", "Low")
			weight.config(width=7)
			weight.grid(row=i, column=2)
			weights.append(var1)
			
			sentimentStr = StringVar(toplevel)
			sentimentStr.set(self.attribute1_values[i][2])
			sentiment = OptionMenu(self.attribute_frame, sentimentStr, "Positive", "Negative")
			sentiment.config(width=7)
			sentiment.grid(row=i, column=3)
			sentiments.append(sentimentStr)

		set_attribute = lambda: self.set_attribute_values(wordBoxes, weights, sentiments)

		Button(self.attribute_frame, text="Save", command=set_attribute).grid(row=4, column=0,pady=10, padx=5)
	

	def get_control_values(self, controls):
		values = []
		for control in controls:
			value = control.get()
			values.append(value)
		return values

	def set_attribute_values(self, words, weights, sentiments):
		self.words = self.get_control_values(words)
		
		newWeights = []
		for weight in weights:
			if weight.get()== "High":
				newWeights.append(3)
			elif weight.get() == "Medium":
				newWeights.append(2)
			else:
				newWeights.append(1)

		newSentiments = []
		for sentiment in sentiments:
			if sentiment.get() == "Positive":
				newSentiments.append(1)
			else:
				newSentiments.append(-1)

		self.weights = newWeights
		self.sentiments = newSentiments
		self.attribute1_values = zip(self.words,self.weights,self.sentiments)


root=Tk()
app = App(root)
root.mainloop()
