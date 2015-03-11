from nltk.corpus import movie_reviews
from nltk.stem import SnowballStemmer
from nltk import FreqDist
from time import time
from random import shuffle

class ScoreTrainer:
  '''
  With help from the nltk documentation: http://www.nltk.org/book/ch06.html#ref-document-classify-all-words    
  '''
  def __init__(self):
    self.stemmer = SnowballStemmer('english')
    self.dictionary = self.initDictionary()
    
    categories = movie_reviews.categories()
    documents = [(fileid, category) 
                    for category in categories
                    for fileid in movie_reviews.fileids(category)]
    shuffle(documents)                
                    
    t0 = time()
    ctr = 0
    for document in documents:
      self.parseDocument(document)
      ctr += 1
      print ctr
    print "Took", time() - t0, "s"
    
    for key in self.dictionary.keys():
      print key, ":", self.dictionary[key]
      raw_input()
      
  def initDictionary(self):
    words = FreqDist(word.lower() for word in movie_reviews.words())
    
    myDict = dict()
    for word in words.keys()[:2000]:
      root = self.rootword(word)
      myDict[root] = {"pos": 0, "neg": 0}
    
    return myDict
                    
  def parseDocument(self, document):
    words = movie_reviews.words(document[0])
    keys = self.dictionary.keys()
    
    for word in words:
      root = self.rootword(word)
      if root in keys:
        sentiment = document[1]
        self.dictionary[root][sentiment] += 1
        
  def rootword(self, word):
    return self.stemmer.stem(word) 

    
    
ScoreTrainer()
    