'''
SearchPacket! Made of individual attributes. This will be passed into the scorer for some 
sweet scoring action. Radical, dude!

@author:  Justin A. Middleton
@date:    8 March 2015
'''
import unittest
from SearchPacket import SearchPacket

class SearchPacketTests(unittest.TestCase):
  def setUp(self):
    self.packet = SearchPacket()

#add 
  #pass
  def test000_000_add(self):
    name = "test"
    words = ["test"]
    weights = [3]
    sentiments = [1]
    distances = [1]
    self.packet.add(name, words, weights, sentiments, distances)
    self.assertEquals(len(self.packet.attributes), 1)
    
  #fail
  def test000_900_add_badDimensions(self):
    correctError = "add: "
    try:
      name = "test"
      words = ["test"]
      weights = [3]
      sentiments = [1, 1]
      distances = [1]
      self.packet.add(name, words, weights, sentiments, distances)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      print str(e)
      self.fail("Error: wrong error.")
      
  '''def test000_901_add_duplicateAttribute(self):
    correctError = "add: "
    try:
      name1 = "test"
      name2 = "test"
      
      words = ["test"]
      weights = [3]
      sentiments = [1]
      distances = [1]
      
      self.packet.add(name1, words, weights, sentiments, distances)
      self.packet.add(name2, words, weights, sentiments, distances)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      print str(e)
      self.fail("Error: wrong error.")'''
      
#remove
  #pass
  def test100_000_remove(self):
    name = "test"
    words = ["test"]
    weights = [3]
    sentiments = [1]
    distances = [1]
    self.packet.add(name, words, weights, sentiments, distances)
    self.packet.remove(name)
    self.assertEquals(len(self.packet.attributes), 0)
    
  #fail
  def test100_900_remove_notInDictionary(self):
    correctError = "remove: "
    try:
      name = "test"
      words = ["test"]
      weights = [3]
      sentiments = [1]
      distances = [1]
      self.packet.add(name, words, weights, sentiments, distances)
      self.packet.remove("not here")
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      print str(e)
      self.fail("Error: wrong error.")
      
#makeSearchItem
  #pass
  def test200_000_makeSearchItem(self):
    testDict = self.packet.makeSearchItem("test", 3, 1, 1)
    self.assertEquals(testDict["word"], "test")
    self.assertEquals(testDict["weight"], 3)
    self.assertEquals(testDict["sentiment"], 1)
    self.assertEquals(testDict["distance"], 1)
    self.assertEquals(testDict["tokens"], ["test"])
    self.assertEquals(testDict["lemmas"], ["test"])
    self.assertEquals(testDict["isPhrase"], False)
    
  def test200_001_makeSearchItem_phrase(self):
    testDict = self.packet.makeSearchItem("test cases", 3, 1, 1)
    self.assertEquals(testDict["word"], "test cases")
    self.assertEquals(testDict["weight"], 3)
    self.assertEquals(testDict["sentiment"], 1)
    self.assertEquals(testDict["distance"], 1)
    self.assertEquals(testDict["tokens"], ["test", "cases"])
    self.assertEquals(testDict["lemmas"], ["test", "case"])
    self.assertEquals(testDict["isPhrase"], True)
    
  #fail
  def test200_900_makeSearchItem_badWeight(self):
    correctError = "makeSearchItem: "
    try:
      self.packet.makeSearchItem("test", 4, 1, 1)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      print str(e)
      self.fail("Error: wrong error.")
      
  def test200_900_makeSearchItem_badSentiment(self):
    correctError = "makeSearchItem: "
    try:
      self.packet.makeSearchItem("test", 3, 0, 1)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      print str(e)
      self.fail("Error: wrong error.")
      
  def test200_900_makeSearchItem_badDistance(self):
    correctError = "makeSearchItem: "
    try:
      self.packet.makeSearchItem("test", 3, 1, -1)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      print str(e)
      self.fail("Error: wrong error.")
      
#getAttributes
  #pass
  def test300_000_getAttributes(self):
    self.packet.add("test1", ["test"], [1], [1], [1])
    self.packet.add("test2", ["another"], [2], [-1], [2])
    attrs = self.packet.getAttributes()
    
    names = ("test1", "test2")
    count = 0
    for name, attr in attrs:
      self.assertEquals(name, names[count])
      count += 1
    self.assertEquals(count, 2)
      
if __name__ == '__main__':
  unittest.main()  
    