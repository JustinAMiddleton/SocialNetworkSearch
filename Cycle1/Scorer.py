#from nltk.corpus import movie_reviews
from textblob import TextBlob, Word

'''
This class will be fed words and their significance.
It will score a sentence based on whether those words appear,
and if they do, how significant they are to our attribute.

@author:  Justin A. Middleton
@date:    24 Feb 2015
'''
class Scorer():
  '''
  What I expect: a list of tuples
    First element: word
    Second element: significance, given in 1, 2, or 3
    Third element: expected sentiment, either 1 (pos) or -1 (neg)
  '''
  def __init__(self, words=None):      
    self.data = dict()
    for word, weight, sent in words:
      self.data[word] = (weight, sent)
    print self.data
          
  '''
  Scores an input sentence, currently using the pattern analyzer
  as part of text blob. 
  Ignore subjectivity. Use absolute value of polarity.
  '''
  def score(self, text):
    blob = TextBlob(text)
    score = 0
    
    '''Goes through each word in the text, checks if it's in it.'''
    for word in blob.words:
      #correctWord = self.rootword(word)
      correctWord = word
      if correctWord in self.data:
        weight = self.data[correctWord][0]
        polarity = self.data[correctWord][1] * blob.sentiment.polarity
        
        #If polarity is negative, that means the expected polarity conflicts with actual polarity. Ignore.
        if polarity > 0:
          score += weight * polarity
        
    return score
      
  '''
  Spellchecks, then lemmatizes (gets rid of plural and conjugations).
  TODO: Doesn't play well with verb unless I provide parameter 'v'?
  '''
  def rootword(self, text):
    return Word(text).correct().lemmatize()
  
'''
Simple main function right here. It will definitely change as it
gives way to real unit tests.
'''
if __name__ == "__main__":
  words = ["happy", "joy", "buddies", "good", "love", "hate"]
  weights = [1,3,2,2,1,1]
  targetSentiment = [1,1,1,1,1,-1]
  s = Scorer(zip(words,weights,targetSentiment))
    
  test = ""
  while True:
    print "Enter input: "
    test = raw_input()
    print s.score(test)
    print
