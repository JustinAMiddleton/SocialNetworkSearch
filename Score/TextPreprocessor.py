from Lemmatizer import Lemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize

class TextPreprocessor:
  def __init__(self):
    self.lemmatizer = Lemmatizer()
    
  def preprocess(self, text):
    preprocessed = {}
    text = text.lower()
    preprocessed["original"] = text.lower()
    
    tokens = word_tokenize(text)
    #spellcheck
    
  def spellcheck(self):
    pass