import RedditObject

class PrimitiveScore:
  def __init__(self):
    self.word = ''
    
  '''
  The primitive score just counts how many times the scorer's word appears
  in the RedditObject's text.
  '''
  def score(self, redditObj):
    if not isinstance(redditObj, RedditObject.RedditObject):
      print "Not a RedditObject"
      return 0
      
    if self.word == '':
      print "Word not set."
      return 0
      
    str = redditObj.text
    score = str.count(self.word)
    redditObj.setScore(score)
    return score
    
  '''
  Sets the scorer's word.
  '''
  def setWord(self, word):
    self.word = word