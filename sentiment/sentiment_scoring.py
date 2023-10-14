import numpy as np
from . import SentimentVector
import math

def dot_similarity(a: SentimentVector, b: SentimentVector):
  return np.dot(a.vector, b.vector)

def cosine_similarity(a: SentimentVector, b: SentimentVector):
  def abs_norm(v):
    return abs(math.sqrt(np.dot(v, v)))

  return np.dot(a.vector, b.vector) / (abs_norm(a.vector) * abs_norm(b.vector))

def weighted_combination(content_score, sentiment_score, w_content=1, w_sentiment=1):
  return content_score * w_content + sentiment_score * w_sentiment

# We want to allow specifying a custom weighting model, but it can only be done through base classes
# Therefore, we create a subclass at runtime
def make_sentiment_weighting_mdl_class(content_weighting_mdl_class, similarity_fun=cosine_similarity, combination_fun=weighted_combination):
  return type('SentimentAndContentScorer', (content_weighting_mdl_class, ), {
    "use_final": True,
    "final": final_weighting,
    "set_query_sentiment_vector": set_query_sentiment_vector,
    "similarity_function": staticmethod(similarity_fun),
    "combination_function": staticmethod(combination_fun)
  })

def set_query_sentiment_vector(self, query_sentiment_vector):
  self.query_sentiment_vector = query_sentiment_vector

def final_weighting(self, searcher, docnum, content_score):
  # Call the original final method
  content_score = super(type(self), self).final(searcher, docnum, content_score)

  if not self.query_sentiment_vector:
    return content_score

  # Retrieve the sentiment vector
  vector = searcher.stored_fields(docnum)['sentiment']
  sentiment_score = self.similarity_function(vector, self.query_sentiment_vector)
  return self.combination_function(content_score, sentiment_score)