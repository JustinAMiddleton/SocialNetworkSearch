from nltk.corpus import movie_reviews, stopwords as Stopwords
from nltk.stem import SnowballStemmer
from string import punctuation as Punctuation
from time import time
from random import shuffle

class ScoreTrainer:
  '''
  With help from the nltk documentation: http://www.nltk.org/book/ch06.html#ref-document-classify-all-words    
  '''
  def __init__(self):
    self.dictionary = dict()
    self.stemmer = SnowballStemmer('english')
    
    categories = movie_reviews.categories()
    documents = [(fileid, category) 
                    for category in categories
                    for fileid in movie_reviews.fileids(category)]
    shuffle(documents)                
    documents = documents[:500]
                    
    t0 = time()
    ctr = 0
    for document in documents:
      self.parseDocument(document)
      ctr += 1
      print ctr
    print "Took", time() - t0, "s"
    
    for key in self.dictionary.keys():
      print key, ":", self.dictionary[key]
      raw_input
    
                    
  def parseDocument(self, document):
    words = movie_reviews.words(document[0])
    stopwords = set(Stopwords.words())
    punctuation = set(Punctuation)
    
    for word in words:
      if word not in stopwords and word not in punctuation:
        root = self.rootword(word)
        self.addToDict(root, document[1])
        
  def rootword(self, word):
    return self.stemmer.stem(word)
        
  def addToDict(self, word, sentiment):
    if word not in self.dictionary.keys():
      self.dictionary[word] = {'pos':0, 'neg':0}
    
    self.dictionary[word][sentiment] += 1
    
    
ScoreTrainer()
    