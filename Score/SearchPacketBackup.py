'''
SearchPacket! Made of individual attributes. This will be passed into the scorer for some 
sweet scoring action. Radical, dude!

@author:  Justin A. Middleton
@date:    12 March 2015
'''
from nltk import word_tokenize
from Attribute import Attribute
#from Lemmatizer import Lemmatizer

class SearchPacket:
  '''
  The attributes as held in this class are different than the attribute class.
  That class is especially suited to accepted GUI input and providing GUI output.
  Attributes here will be more focused on collecting all related information into a single area.
  '''
  def __init__(self, attributes = None):
    '''
    Dictionary of attributes: name is mapped to list of words/search items represented as dictionaries.
    Visualization:
      Attribute1 [
        SearchItem1 {
          word, weight, sentiment, distance, tokens, lemmas, isPhrase
        }
        SearchItem2 {
          word, weight, sentiment, distance, tokens, lemmas, isPhrase
        }
        ...
      ]
      Attribute2 [...]
    '''
    self.attributes = {}
    if attributes is not None:
      self.addAll(attributes)
  
  '''
  Takes the attribute input from the constructor and adds them all.
  '''
  def addAll(self, attributes):
    for attr in attributes:
      name = attr.get_name()
      words = attr.get_words()
      weights = attr.get_weights()
      sentiments = attr.get_sentiments()        
      
      try:
        self.add(name, words, weights, sentiments)
      except ValueError, e:
        continue
        
    if len(self.attributes.keys()) == 0:
      raiseValueError("addAll: No valid attributes for which to search.")
    
  '''
  Add a new attribute to the dictionary. 
  Duplicates count as overwriting.  
    name:       str
    words:      list of str
    weights:    list of int (1 through 3)
    sentiment:  list of int (-1 or 1)
    distances:  list of int (>= 0)
    
  Returns number of attributes.
  #RECENT: Removed distance
  '''
  def add(self, name, words, weights, sentiments, distances=None):
    if name is None or name == "":
      raise ValueError("add: Attribute must have a valid name.")
    if name in self.attributes.keys():
      raise ValueError("add: The attribute must have a unique name.")
    if words is None or weights is None or sentiments is None:
      raise ValueError("add: Not all attribute fields set.")
    if len(words) != len(weights) or len(words) != len(sentiments): # or len(words) != len(distances):
      raise ValueError("add: Number of arguments in each list don't match.")
      
    searchItems = []
    for word, weight, sentiment in zip(words, weights, sentiments):
      if word == "": 
        continue        
        
      #TODO: Is there something else I should do with the error, rather than printing it?
      try: 
        newItem = self.makeSearchItem(word, weight, sentiment)
      except ValueError, e:
        continue
        
      searchItems.append(newItem)
      
    if len(searchItems) == 0:
      raise ValueError("add: There must be at least one valid word.")
    self.attributes[name] = searchItems
    
    return len(self.attributes)

  '''
  Turn a collection of search item information into a dictionary.  
    word:      str
    weight:    int
    sentiment: int
    distance:  int
  '''
  def makeSearchItem(self, word, weight, sentiment, distance = None):
    if weight not in range(1, 4):
      raise ValueError("makeSearchItem: bad weight for '%s', %d not in 1 through 3." % (word, weight))
    if sentiment not in (-1, 1):
      raise ValueError("makeSearchItem: bad sentiment for '%s', %d not -1 or 1." % (word, sentiment))
    #if distance < 0:
    #  raise ValueError("makeSearchItem: bad distance for '%s', must be greater than 0." % word)
      
    word = word.lower()
    searchItem = {"word": word, "weight": weight, "sentiment": sentiment}
    
    tokens = word_tokenize(word)
    #lemmas = Lemmatizer().lemmatizeTokens(tokens)        
    searchItem["tokens"] = tokens
    #searchItem["lemmas"] = lemmas
    
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
      
  '''
  Makes a query  based on every word in the search items.
  Returns the query as a string, every search item connected with an "OR".
  '''
  def getQuery(self):
    query = ""
    attributeQueries = []
    for attribute in self.attributes.keys():
      words = []
      for searchItem in self.attributes[attribute]:
        if searchItem["isPhrase"]:
          words.append('\'%s\'' % searchItem["word"]) 
        else:
          words.append(searchItem["word"])

      query = " OR ".join(words)
      attributeQueries.append(query)
    
    finalQuery = " OR ".join(attributeQueries)
    return finalQuery      
        