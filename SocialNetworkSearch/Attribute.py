'''

Created on March 11, 2015

@author: Brenden

'''

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
