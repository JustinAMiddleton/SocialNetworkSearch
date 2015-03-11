'''
SearchPacket! Made of individual attributes. This will be passed into the scorer for some 
sweet scoring action. Radical, dude!

@author:  Justin A. Middleton
@date:    8 March 2015
'''
from nltk import word_tokenize
from Lemmatizer import Lemmatizer

class SearchPacket:
  '''Really, just instantiate an empty dictionary.'''
  def __init__(self):
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

    
  '''
  Add a new attribute to the dictionary. 
  Duplicates count as overwriting.  
    name:       str
    words:      list of str
    weights:    list of int (1 through 3)
    sentiment:  list of int (-1 or 1)
    distances:  list of int (>= 0)
    
  Returns number of attributes.
  '''
  def add(self, name, words, weights, sentiments, distances):
    if name == "":
      raise ValueError("add: Attribute must have a valid name.")
    if len(words) != len(weights) or len(words) != len(sentiments) or len(words) != len(distances):
      raise ValueError("add: Number of arguments in each list don't match.")
      
    searchItems = []
    for word, weight, sentiment, distance in zip(words, weights, sentiments, distances):
      if word == "": 
        continue        
        
      #TODO: Is there something else I should do with the error, rather than printing it?
      try: 
        newItem = self.makeSearchItem(word.lower(), weight, sentiment, distance)
      except ValueError, e:
        print e
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
  def makeSearchItem(self, word, weight, sentiment, distance):
    if weight not in range(1, 4):
      raise ValueError("makeSearchItem: bad weight for '%s', %d not in 1 through 3." % (word, weight))
    if sentiment not in (-1, 1):
      raise ValueError("makeSearchItem: bad sentiment for '%s', %d not -1 or 1." % (word, sentiment))
    if distance < 0:
      raise ValueError("makeSearchItem: bad distance for '%s', must be greater than 0." % word)
      
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
        