import numpy as np
from . import SentimentVector
import math

def __norm(v):
  return math.sqrt(np.dot(v, v))

def cosine_similarity(d: SentimentVector, q: SentimentVector):
  return np.dot(d.vector, q.vector) / (__norm(d.vector) * __norm(q.vector))

def dot_similarity(d: SentimentVector, q: SentimentVector):
  return np.dot(d.vector, q.vector)

def normalized_dot_similarity(d: SentimentVector, q: SentimentVector):
  # Divide the dot similarity by the best or worst score achievable

  dot_similarity = np.dot(d.vector, q.vector)

  if dot_similarity >= 0:
    positive_q = q.vector[q.vector > 0]
    ideal_d_dot_similarity = np.dot(positive_q, positive_q)
    return dot_similarity / ideal_d_dot_similarity
  else:
    negative_q = q.vector[q.vector < 0]
    worst_d_dot_similarity = np.dot(negative_q, negative_q)
    return dot_similarity / worst_d_dot_similarity


def linear_combination(content_score, sentiment_score, w_content=1, w_sentiment=1):
  return content_score * w_content + sentiment_score * w_sentiment


import abc

class SentimentWeightingModelMixin(abc.ABC):
  use_final = True

  def final(self, searcher, docnum, content_score):
    content_score = super().final(searcher, docnum, content_score)

    if not self.query_sentiment_vector:
      return content_score

    # Retrieve the sentiment vector
    vector = searcher.stored_fields(docnum)['sentiment']
    sentiment_score = self.vector_similarity_function(vector, self.query_sentiment_vector)
    return self.score_combination_function(content_score, sentiment_score)
  
  def set_query_sentiment_vector(self, query_sentiment_vector):
    self.query_sentiment_vector = query_sentiment_vector

  @abc.abstractmethod
  def score_combination_function(self, content, sentiment):
    pass

  @abc.abstractmethod
  def vector_similarity_function(self, document, query):
    pass

from whoosh import scoring
class DefaultWeightingModel(SentimentWeightingModelMixin, scoring.BM25F):
  def __init__(self, sentiment_weight = 10, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.sentiment_weight = sentiment_weight

  def score_combination_function(self, content, sentiment):
    return linear_combination(content, sentiment, w_sentiment=self.sentiment_weight)

  def vector_similarity_function(self, document, query):
    return normalized_dot_similarity(document, query)