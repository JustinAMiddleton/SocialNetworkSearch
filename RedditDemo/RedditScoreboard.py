import RedditObject
from pprint import pprint

class RedditScoreboard:
  def __init__(self):
    self.board = dict()
    
  '''
  Adds the score in a reddit object to the user's current score.
  If the user has not been observed before, it adds them.
  '''
  def add(self, redditObj):
    if not isinstance(redditObj, RedditObject.RedditObject):
      print "RedditScoreboard.add: Invalid input"
      return
    
    if redditObj.author in self.board:
      self.board[redditObj.author] += redditObj.score
    else:
      self.board[redditObj.author] = redditObj.score
    #print redditObj.author, redditObj.score
      
  '''
  Prints the top ten authors in the list, by score.
  '''
  def topTen(self):
    sorted_board = sorted(self.board.iterkeys(), key=lambda x:self.board[x], reverse=True)
    
    print '\n%-20s%-5s' % ("name", "count"), "\n"
    for x in range(0,10):
      print '%-20s%-5i' % (sorted_board[x], self.board[sorted_board[x]])
