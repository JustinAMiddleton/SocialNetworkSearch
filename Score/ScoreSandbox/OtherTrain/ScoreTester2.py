from nltk.corpus import movie_reviews
from nltk.stem import SnowballStemmer

class ScoreTester:   
  '''
  When testing, we must pass in:
    What dictionary we're using to evaluate words.
    Whether or not we expect stemming.
  '''
  def test(self, scorer=None, stem=False):
    if scorer is None:
      print "No scorer to use."
      return 0
      
    stem = SnowballStemmer('english')
    documents = self.getDocuments()
    correct = 0
    
    for fileid, category in documents:
      score = scorer.score(

  '''
  Returns a list of documents and their labels from the corpus.
  '''
  def getDocuments(self):
    categories = movie_reviews.categories()
    documents = [(fileid, category) 
                    for category in categories
                    for fileid in movie_reviews.fileids(category)]
    return documents