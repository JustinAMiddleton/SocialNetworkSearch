from nltk.corpus import movie_reviews

class ScoreTrainer:
  def __init__(self, stem=False):
    self.dictionary = self.getDictionary()
    
  def getDictionary(self):
    f = open('AFINN-111.txt', 'r')
    words = {}
    
    for line in f:
      splitLine = line.split('\t')
      word = splitLine[0]
      sentiment = int(splitLine[1])
      words[word] = sentiment
      
    return words
    
  def predict(self, text):
    score = 0
    maxScore = float(0)
    for word in text:
      word = word.encode('ascii')
      if word in self.dictionary.keys():
        #print word, self.dictionary[word]
        score += self.dictionary[word]
        maxScore += 5
        
    rating = ""
    if score > 0:
      rating = "pos"
    else:
      rating = "neg"
      
    return rating
    
  def test(self):
    documents = [(fileid, rating)
                  for rating in movie_reviews.categories()
                  for fileid in movie_reviews.fileids(rating)]

    correct = 0
    index = 0
    for document, actualRating in documents:
      predictedRating = self.predict(movie_reviews.words(document))
      if predictedRating == actualRating:
        correct += 1
        
      index += 1
      print index
        
    print "Accuracy: ", float(correct) / len(documents)
    #Returns an accuracy of .637
      
ScoreTrainer().test()
