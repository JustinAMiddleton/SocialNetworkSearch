'''

Created on March 11, 2015

@author: Brenden

'''

class Attribute():
	def __init__(self, name = "Attribute", attrWeight = 1,
			words = None, weights = None, sentiments = None):
		self.name = name
		self.attrWeight = attrWeight
		self.words = words
		self.weights = weights
		self.sentiments = sentiments
		
	def __eq__(self, other):
		if self.name != other.name:
			return False
		if self.attrWeight != other.attrWeight:
			return False
		if self.words != other.words:
			return False
		if self.weights != other.weights:
			return False
		if self.sentiments != other.sentiments:
			return False
		
		return True

	def set_name(self, name):
		self.name = name
		
	def set_attr_weight(self, weight):
		if weight == "High":
			self.attrWeight = 3
		elif weight == "Medium":
			self.attrWeight = 2
		else:
			self.attrWeight = 1
	
	def set_words(self, words):
		self.words = words

	'''Expects a list of strings.'''
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
		
	'''Expects a list of numbers.'''
	def set_weights_nums(self, weights):
		self.weights = weights

	'''Expects a list of strings.'''
	def set_sentiments(self, sentiments):
		newSentiments = []
		for sentiment in sentiments:
			if sentiment == "Positive":
				newSentiments.append(1)
			else:
				newSentiments.append(-1)
		self.sentiments = newSentiments
		
	'''Expects a list of numbers.'''
	def set_sentiments_nums(self, sentiments):
		self.sentiments = sentiments

	def get_word(self, index):
		return self.words[index]

	def get_weight(self, index):
		if self.weights[index] == 3:
			return "High"
		elif self.weights[index] == 2:
			return "Medium"
		else:
			return "Low"
			
	def get_weight_num(self, index):
		return self.weights[index]

	def get_sentiment(self, index):
		if self.sentiments[index] == 1:
			return "Positive"
		else:
			return "Negative"
			
	def get_sentiment_num(self, index):
		return self.sentiments[index]
			
	def get_size(self):
		return len(self.words)
			
	'''
	The following functions are for bulk processing in the SearchPacket class.
	'''
	
	'''Gets the attribute name.'''
	def get_name(self):
		return self.name
		
	'''Gets the attribute weight.'''
	def get_attr_weight(self):
		return self.attrWeight
			
	'''Gets the entire list of attribute words.'''
	def get_words(self):
		return self.words
		
	'''Gets the entire list of attribute weights.'''
	def get_weights(self):
		return self.weights
		
	'''Gets the entire list of attribute expected sentiments.'''
	def get_sentiments(self):
		return self.sentiments
		
	def get_max_score(self):
		return sum(self.weights)
