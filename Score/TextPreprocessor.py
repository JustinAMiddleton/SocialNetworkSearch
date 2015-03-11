from Lemmatizer import Lemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from textblob import TextBlob
from enchant.checker import SpellChecker

class TextPreprocessor:
  def __init__(self):
    self.lemmatizer = Lemmatizer()
    
  def preprocess(self, text):
    preprocessed = {}
    text = text.lower()
    preprocessed["original"] = text.lower()
    
    spellchecked = self.spellcheck(text)
    tokens = word_tokenize(text)
    #spellcheck
    
  '''
  Uses the textblob library to attempt to check the speller.
  The textblob checker is based on Peter Norvig's implementation: http://norvig.com/spell-correct.html
  It has about a 70% accuracy.
  '''
  def spellcheck(self, text):
    '''sentence = TextBlob(text)
    print sentence.correct()
    return str(sentence.correct())'''
    return text
    