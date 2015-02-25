from RedditDemo.RedditCrawler import RedditCrawler
from TwitterDemo.TwitterCrawler import TwitterCrawler
import GooglePlusDemo.GooglePlusSearch

class Interface:
  def __init__(self):
    self.red = RedditCrawler()
    self.twit = TwitterCrawler()
    
    self.twit.login()

  def main(self):
    word = raw_input('Enter a search term: ')
    
    print "###################","\nProcessing Reddit...", "\n###################\n"
    self.red.search(word)
    
    print "###################","\nProcessing Twitter... (First 100)", "\n###################\n"
    self.twit.BasicSearch(word)
    
    print "###################","\nProcessing Google...", "\n###################\n"
    GooglePlusDemo.GooglePlusSearch.mySearch(word)
    
if __name__ == "__main__":
  Interface().main()
    