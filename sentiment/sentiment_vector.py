import numpy as np
import math

class SentimentVector:
  SENTIMENTS = np.array([
    'anger',
    'disgust',
    'fear',
    'joy',
    'neutral',
    'sadness',
    'surprise'
  ])


  def __init__(self, value = None):
    if value is None:
      self.vector = np.zeros(SentimentVector.SENTIMENTS.shape, dtype=float)
      return

    if isinstance(value, SentimentVector):
      self.vector = value.vector

    elif isinstance(value, str):
      self.vector = (SentimentVector.SENTIMENTS == value).astype(float)
      if not np.any(self.vector != 0):
        raise ValueError(f"Unknown emotion {value}")
    
    else:
      # Anything that can be cast to an array with the correct shape and type is fine.
      value = np.array(list(value)).astype(float)
      if value.shape != SentimentVector.SENTIMENTS.shape:
        raise ValueError(f"Bad shape {value.shape} vs {SentimentVector.SENTIMENTS.shape}")
      self.vector = value
      

  def __and__(self, other):
    # Documents that fully match the vectors have an advantage over those that have a partial match or no match at all.
    other = SentimentVector(other)
    return SentimentVector(np.sign(self.vector + other.vector))
  

  def __invert__(self):
    # Documents that match the vector are penalized.
    return SentimentVector(-self.vector)
  
  
  def __or__(self, other):
    # Because of how we defined AND, OR is unintuitive to me.
    # I tried to apply De Morgan...
    return self.__and__(other) # Approved by De Morgan™
  

  def __repr__(self):
    return f"{self.__class__.__name__}({np.array_repr(self.vector, max_line_width=math.inf, precision=3)})"
  
  def human_readable(self, thresh=0.2):
    def sentstr(i):
      return f"{self.SENTIMENTS[i]}({self.vector[i]:.3f})"

    strongest = np.flip(np.argsort(self.vector))
    strong = [sentstr(i) for i in strongest if self.vector[i] > thresh]
    if len(strong) == 0:
      strong = (sentstr(strongest[0]), )
    return " AND ".join(strong)