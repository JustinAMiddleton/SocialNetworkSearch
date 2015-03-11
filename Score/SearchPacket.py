'''
SearchPacket! Made of individual attributes. This will be passed into the scorer for some 
sweet scoring action. Radical, dude!

@author:  Justin A. Middleton
@date:    8 March 2015
@TODO:    Disregard empty words.
'''
from nltk import word_tokenize
from Lemmatizer import Lemmatizer

class SearchPacket:
  '''Really, just instantiate an empty dictionary.'''
  def __init__(self):
    self.attributes = {}
    
  '''
  Add a new attribute to the dictionary. 
  Duplicates count as overwriting.  
    name:       str
    words:      list of str
    weights:    list of int (1-3)
    sentiment:  list of int (-1, 1)
    distances:  list of int
    
  Returns number of attributes.
  '''
  def add(self, name, words, weights, sentiments, distances):
    if len(words) != len(weights) or len(words) != len(sentiments) or len(words) != len(distances):
      raise ValueError("add: Number of arguments in each list don't match.")
      
    searchItems = []
    for word, weight, sentiment, distance in zip(words, weights, sentiments, distances):
      searchItems.append(self.makeSearchItem(word.lower(), weight, sentiment, distance))
    self.attributes[name] = searchItems
    
    return len(self.attributes)

  '''
  Turn a collection of search item information into a dictionary.  
    word:      str
    weight:    int
    sentiment: int
    distance:  int
  '''
  def makeSearchItem(self, word, weight, sentiment, distance):
    if weight not in range(1, 4):
      raise ValueError("makeSearchItem: bad weight, %d not in 1 through 3." % weight)
    if sentiment not in (-1, 1):
      raise ValueError("makeSearchItem: bad sentiment, %d not -1 or 1." % sentiment)
    if distance < 0:
      raise ValueError("makeSearchItem: bad distance, must be greater than 0.")
      
    searchItem = {"word": word, "weight": weight, "sentiment": sentiment,
      "distance": distance}
    
    tokens = word_tokenize(word)
    lemmas = Lemmatizer().lemmatizeTokens(tokens)        
    searchItem["tokens"] = tokens
    searchItem["lemmas"] = lemmas
    
    #Record if it's a phrase.
    if len(tokens) == 1:
      searchItem["isPhrase"] = False
    else:
      searchItem["isPhrase"] = True
    
    return searchItem
    
  '''
  Removes a given attribute from the dictionary.  
    name: str
  '''
  def remove(self, name):
    if name not in self.attributes.keys():
      raise ValueError("remove: Attribute not in dictionary.")
      
    del self.attributes[name]
    
  '''
  Generator for the attributes held in this packet.
  '''
  def getAttributes(self):
    for key in self.attributes.keys():
      yield key, self.attributes[key]
        