from Tkinter import *
from RedditCrawler import RedditCrawler

class Interface:
  def main(self):
    red = RedditCrawler()
    word = raw_input('Enter a search term: ')
    red.search(word)
    
if __name__ == "__main__":
  Interface().main()
    