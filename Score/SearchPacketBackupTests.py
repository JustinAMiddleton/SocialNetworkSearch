'''
SearchPacket! Made of individual attributes. This will be passed into the scorer for some 
sweet scoring action. Radical, dude!

@author:  Justin A. Middleton
@date:    8 March 2015
'''
import unittest
from SearchPacket import SearchPacket
from Attribute import Attribute

class SearchPacketTests(unittest.TestCase):
  def setUp(self):
    self.packet = SearchPacket()
    
    self.attr1 = Attribute()
    self.attr1.name = "one"
    self.attr1.set_words(["one", "two", "three"])
    self.attr1.set_weights([1,2,3])
    self.attr1.set_sentiments([1,1,1])
    
    self.attr2 = Attribute()
    self.attr2.name = "two"
    self.attr2.set_words(["four", "five", "six"])
    self.attr2.set_weights([3,2,1])
    self.attr2.set_sentiments([-1,1,-1])
    
    self.attrs = [self.attr1, self.attr2]
    
#add 
  #pass
  def test000_000_add(self):
    name = "test"
    words = ["test"]
    weights = [3]
    sentiments = [1]
    distances = [1]
    self.assertEquals(self.packet.add(name, words, weights, sentiments, distances), 1)
    self.assertEquals(len(self.packet.attributes), 1)
    
  '''def test000_001_add_edit(self):    
    name = "test"
    words = ["test"]
    weights1 = [3]
    weights2 = [2]
    sentiments = [1]
    distances = [1]
    self.assertEquals(self.packet.add(name, words, weights1, sentiments, distances), 1)
    self.assertEquals(self.packet.add(name, words, weights2, sentiments, distances), 1)
    self.assertEquals(len(self.packet.attributes), 1)'''
    
  def test000_002_add_moreThanOne(self):
    name = "test1"
    name2 = "test2"
    words = ["test"]
    weights = [3]
    sentiments = [1]
    distances = [1]
    self.packet.add(name, words, weights, sentiments, distances)
    self.assertEquals(self.packet.add(name2, words, weights, sentiments, distances), 2)
    self.assertEquals(len(self.packet.attributes), 2)
    
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
      self.fail(str(e))
      
  def test000_901_add_emptyName(self):
    correctError = "add: "
    try:
      name = ""
      words = ["test"]
      weights = [3]
      sentiments = [1]
      distances = [1]
      self.packet.add(name, words, weights, sentiments, distances)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      self.fail(str(e))
      
  def test000_902_add_emptyWord(self):
    correctError = "add: "
    try:
      name = "test"
      words = ["", ""]
      weights = [3, 2]
      sentiments = [1, -1]
      distances = [1, 1]
      self.packet.add(name, words, weights, sentiments, distances)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      self.fail(str(e))
      
  '''
  This test should fail because all values have a problem, which means none will be stored,
  which means the full attribute itself cannot be constructed.
  '''
  def test000_903_add_invalidValues(self):
    correctError = "add: "
    try:
      name = "test"
      '''words = ["badWeight", "badSent", "badDistance"]
      weights = [4, 2, 1]
      sentiments = [1, 2, -1]
      distances = [1, 1, -1]'''
      words = ["badWeight", "badSent"]
      weights = [4, 2]
      sentiments = [1, 2]
      self.packet.add(name, words, weights, sentiments)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      self.fail(str(e))
      
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
      self.fail(str(e))
      
#makeSearchItem
  #pass
  def test200_000_makeSearchItem(self):
    testDict = self.packet.makeSearchItem("test", 3, 1, 1)
    self.assertEquals(testDict["word"], "test")
    self.assertEquals(testDict["weight"], 3)
    self.assertEquals(testDict["sentiment"], 1)
    #self.assertEquals(testDict["distance"], 1)
    self.assertEquals(testDict["tokens"], ["test"])
    #self.assertEquals(testDict["lemmas"], ["test"])
    self.assertEquals(testDict["isPhrase"], False)
    
  def test200_001_makeSearchItem_phrase(self):
    testDict = self.packet.makeSearchItem("test cases", 3, 1, 1)
    self.assertEquals(testDict["word"], "test cases")
    self.assertEquals(testDict["weight"], 3)
    self.assertEquals(testDict["sentiment"], 1)
    #self.assertEquals(testDict["distance"], 1)
    self.assertEquals(testDict["tokens"], ["test", "cases"])
    #self.assertEquals(testDict["lemmas"], ["test", "case"])
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
      self.fail(str(e))
      
  def test200_900_makeSearchItem_badSentiment(self):
    correctError = "makeSearchItem: "
    try:
      self.packet.makeSearchItem("test", 3, 0, 1)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      self.fail(str(e))
      
  '''def test200_900_makeSearchItem_badDistance(self):
    correctError = "makeSearchItem: "
    try:
      self.packet.makeSearchItem("test", 3, 1, -1)
      self.fail("Error: no error!")
    except ValueError, e:
      self.assertEqual(correctError, str(e)[:len(correctError)])
    except Exception, e:
      self.fail(str(e))'''
      
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
    
#getQuery
  #pass
  def test400_000_getQuery(self):
    name = "test"
    words = ["one", "two", "three"]
    weights = [3, 2, 1]
    sentiments = [1, 1, 1]
    distances = [1, 1, 1]
    self.packet.add(name, words, weights, sentiments, distances)
    
    name2 = "test2"
    words2 = ["four", "five"]
    weights2 = [3, 2]
    sentiments2 = [-1, -1]
    distances2 = [1, 1]
    self.packet.add(name2, words2, weights2, sentiments2, distances2)
    
    self.assertEquals(self.packet.getQuery(), "one OR two OR three OR four OR five")

  def test400_001_getQuery_withPhrases(self):
    name = "test"
    words = ["zero", "one", "two three"]
    weights = [3, 2, 1]
    sentiments = [1, 1, 1]
    distances = [1, 1, 1]
    self.packet.add(name, words, weights, sentiments, distances)
    
    name2 = "test2"
    words2 = ["four five", "six"]
    weights2 = [3, 2]
    sentiments2 = [-1, -1]
    distances2 = [1, 1]
    self.packet.add(name2, words2, weights2, sentiments2, distances2)
    
    self.assertEquals(self.packet.getQuery(), "zero OR one OR 'two three' OR 'four five' OR six")        
    
#__init__
  #pass
  def test500_000_init(self):
    testPacket = SearchPacket(self.attrs)
    self.assertEquals(len(testPacket.attributes), 2)
    
      
if __name__ == '__main__':
  unittest.main()  
    