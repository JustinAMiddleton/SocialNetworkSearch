class RedditObject:
  def __init__(self, title, author, text, time):
    self.title = title
    self.author = author
    self.text = text
    self.time = time
    self.score = 0
    
  def getAuthor(self):
    return self.author
    
  def getScore(self):
    return self.score
    
  def setScore(self, score):
    if not isinstance(score, int):
      print "Score must be int"
      return
      
    self.score = score
    