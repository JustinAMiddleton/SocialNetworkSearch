import unittest
from Lemmatizer import Lemmatizer

class LemmatizerTests(unittest.TestCase):
  def setUp(self):
    self.lemmatizer = Lemmatizer()
    
#lemmatize
  #pass
  def test000_000_lemmatize(self):
    testSentence = "I went to the wonderfully decorated stores with dogs \
      for delicious and lovely chocolate."
    self.assertEquals(self.lemmatizer.lemmatize(testSentence),
      "I go to the wonderfully decorate store with dog for delicious and lovely chocolate .")
  
  def test000_001_lemmatize(self):
    testSentence = "dogs cats spotted under mice cutting greased scared"
    self.assertEquals(self.lemmatizer.lemmatize(testSentence),
      "dog cat spot under mouse cut grease scared")
      
  def test000_002_lemmatize(self):
    self.assertEquals(self.lemmatizer.lemmatize("loving"), "love")
    
  def test000_003_lemmatize(self):
    self.assertEquals(self.lemmatizer.lemmatize(""), "")
    
if __name__ == '__main__':
  unittest.main()  
    