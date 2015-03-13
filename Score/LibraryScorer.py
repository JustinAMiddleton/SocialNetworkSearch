class LibraryScorer:
  def __init__(self, searchpacket):
    self.packet = searchpacket
    
  def score(self, text):
    scores = {}
    for key, attr in self.packet.getAttributes():
      score = 0
      for searchword in attr:
        if searchword["word"] in text:
          score += searchword["weight"]
      scores[key] = score