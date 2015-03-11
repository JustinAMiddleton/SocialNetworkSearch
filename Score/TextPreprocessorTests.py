import unittest
from Score.TextPreprocessor import TextPreprocessor

class TextPreprocessorTests(unittest.TestCase):
  def setUp(self):
    self.tpp = TextPreprocessor()
    
  def test000_000_preprocess_caps(self):
    test = "iNcoNSIstent CaPITAlizaTION"
    self.tpp.preprocess(test)
    
if __name__ == "__main__":
  unittest.main()