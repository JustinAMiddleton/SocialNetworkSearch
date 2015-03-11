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
    index = 0
    for document, actualRating in documents:
      predictedRating = scorer.predict(movie_reviews.words(document))
      if predictedRating == actualRating:
        correct += 1
        
      index += 1
      print index
        
    print "Accuracy: ", float(correct) / len(documents)
    #Returns an accuracy of .637
      
  '''
  For a given text, returns whether we think the sentiment is 
  positive (pos) or negative (neg).
  '''
  def predict(self, text):
    

  '''
  Returns a list of documents and their labels from the corpus.
  '''
  def getDocuments(self):
    categories = movie_reviews.categories()
    documents = [(fileid, category) 
                    for category in categories
                    for fileid in movie_reviews.fileids(category)]
    return documents