import unittest
from TextPreprocessor import TextPreprocessor

class TextPreprocessorTests(unittest.TestCase):
  def setUp(self):
    self.tpp = TextPreprocessor()

#preprocess
  #pass
  def test000_000_preprocess_caps(self):
    test = "iNcoNSIstent CaPITAlizaTION"
    self.tpp.preprocess(test)
    
#spellcheck
  #pass
  def test100_000_spellcheck2(self):
    testSentence = "I havv goood speeling"
    correctSentence = "I have good spelling"
    self.assertEquals(self.tpp.spellcheck(testSentence), correctSentence)
    
  def test100_001_spellcheck2(self):
    testSentence = "omg i dont kno wuts hapening"
    correctSentence = "omg i dont know whats happening"
    self.assertEquals(self.tpp.spellcheck(testSentence), correctSentence)

  def test100_002_spellcheck3(self):
    testSentence = "test tets tast yest"
    correctSentence = "test test test test"
    self.assertEquals(self.tpp.spellcheck(testSentence), correctSentence)

  def test100_003_spellcheck4(self):
    testSentence = "dos anyon hav a dolar"
    correctSentence = "does anyone have a dollar"
    self.assertEquals(self.tpp.spellcheck(testSentence), correctSentence)
    
if __name__ == "__main__":
  unittest.main()