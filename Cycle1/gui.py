'''

Created on Feb 18, 2015

@author: Randy

'''

from Tkinter import *
from Interface import Interface
import time
import threading

class GuiThread(threading.Thread):
	def __init__(self, words, weights, sentiments):
		threading.Thread.__init__(self)
		self.words = words
		self.weights = weights
		self.sentiments = sentiments
		self.args = {'location' : 'China'}
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

class App():
	attribute1 = "Attribute 1"
	defAtt = "Define Attribute"

	attribute1_values = [["","","Positive"],["","","Positive"],["","","Positive"],["","","Positive"]]
	words = []
	weights = []
	sentiments = []

	def __init__(self, master): #main window

		frame = Frame(master)
		frame.pack()
		master.title("Whistleblower Analysis")
		#Label(frame, text="Attributes").grid(row=0, column=0, pady=4)
		#Label(frame, text="Web Sites").grid(row=0, column=3)
		Label(frame, text="Attribute").grid(row=1, column=0)
		Button(frame, text=self.defAtt, command=self.defineAttribute).grid(row=1, column=1,pady=4, padx=10)
		#Button(frame, text="X").grid(row=1, column=2, padx=5)
		Button(frame, text="Search", command=self.search).grid(row=2, column=0, padx=10)
		Button(frame, text="Stop", command=self.stop).grid(row=2, column=1, pady=4)
		
		'''var=StringVar(master)
		var.set("Select Date")
	 	option = OptionMenu(frame, var, "Live Stream", "Last 30 Days", 
					"Last 90 Days", "Past Year").grid(row=4, column=3)

		var1 = IntVar()
		Checkbutton(frame, text="Twitter", variable=var1).grid(row=1, column=3, sticky=W, padx=15)
		var2 = IntVar()

		Checkbutton(frame, text="Google+", variable=var2).grid(row=2, column=3, sticky=W, padx=15)

		var3 = IntVar()
		Checkbutton(frame, text="Reddit", variable=var3).grid(row=3, column=3, sticky=W, padx=15)'''
		
	def search(self):
		self.thread = GuiThread(self.words, self.weights, self.sentiments)
		self.thread.start()
		'''zip(self.words,self.weights,self.sentiments)
		self.interface = Interface(self.words, self.weights, self.sentiments)
		self.interface.search(self.interface.get_query(self.words))
		self.interface.score()
		self.interface.db.close()
		time.sleep(1)'''

	def stop(self):
		self.thread.stop()

	def defineAttribute(self): #attribute window
		toplevel= Toplevel()
		toplevel.title('Define Attribute')
		toplevel.geometry('510x170-50+40')
		toplevel.focus_set()
		frame = Frame(toplevel)
		frame.pack()

		wordBoxes = []
		weights = []
		sentiments = []
		for i in range(0,4):
			Label(frame, text="Word "+str(i+1)).grid(row=i, column=0)
			wordBox = Entry(frame)
			wordBox.insert(0, self.attribute1_values[i][0])
			wordBox.grid(row=i, column=1)
			wordBoxes.append(wordBox)
			
			var1 = StringVar(toplevel)
			var1.set("Weight")
			if (self.attribute1_values[i][1] != ""):
				var1.set(self.attribute1_values[i][1])
			weight = OptionMenu(frame, var1, "High", "Medium", "Low")
			weight.config(width=7)
			weight.grid(row=i, column=2)
			weights.append(var1)
			
			sentimentStr = StringVar(toplevel)
			sentimentStr.set(self.attribute1_values[i][2])
			sentiment = OptionMenu(frame, sentimentStr, "Positive", "Negative")
			sentiment.config(width=7)
			sentiment.grid(row=i, column=3)
			sentiments.append(sentimentStr)

		'''set_attribute= lambda: self.set_attribute_values(
				zip(
					self.get_control_values(wordBoxes),
					self.get_control_values(weights),
					self.get_control_values(sentiments)
				))'''
		set_attribute = lambda: self.set_attribute_values(wordBoxes, weights, sentiments)

		Button(frame, text="Save", command=set_attribute).grid(row=4, column=2,pady=10)

	def get_control_values(self, controls):
		values = []
		for control in controls:
			value = control.get()
			values.append(value)
		return values

	def get_wordbox_values(self, boxes):
		words = []
		for box in boxes:
			word = box.get()
			words.append(word)
		return words

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
