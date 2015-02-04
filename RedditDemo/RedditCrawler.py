import Crawler
import praw
import PrimitiveScore
import RedditObject
import RedditScoreboard
#from pprint import pprint
#import time

class RedditCrawler(Crawler.Crawler):
  def __init__(self):
    self.r = praw.Reddit("Reddit Crawler for School Project (No Username)")
    self.scorer = PrimitiveScore.PrimitiveScore()
    self.board = RedditScoreboard.RedditScoreboard()
   
  '''
  Uses the Reddit search API to find results based on a word.
  '''
  def search(self, word):
    self.scorer.setWord(word)
    gen = self.r.search(query=word, limit=1000)
    
    #Reddit generally stores about 1000 results for any search.
    for submission in gen:
      topObj = RedditObject.RedditObject(
                submission.title.encode('utf8'),
                submission.author.name.encode('utf8'),
                submission.selftext.encode('utf8'),
                submission.created)
      self.scorer.score(topObj)
      self.board.add(topObj)
      
      #flat_comments = praw.helpers.flatten_tree(submission.comments)
      #for comment in flat_comments:
      #  pass
    self.board.topTen()
      
if __name__ == "__main__":
  red = RedditCrawler()
  word = raw_input('Enter a search term: ')
  red.search(word)