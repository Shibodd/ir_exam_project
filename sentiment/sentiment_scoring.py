import numpy as np
from . import SentimentVector
import math

def __norm(v):
  return math.sqrt(np.dot(v, v))


def dot_similarity(d: SentimentVector, q: SentimentVector):
  return np.dot(d.vector, q.vector)


def cosine_similarity(d: SentimentVector, q: SentimentVector):
  return np.dot(d.vector, q.vector) / (__norm(d.vector) * __norm(q.vector))


def semi_normalized_dot_similarity(d: SentimentVector, q: SentimentVector):
  # Reward confidence from the inference model (magnitude of the document vector)
  # The relevance of the magnitude of the query vector is not clear, so we don't use it
  return np.dot(d.vector, q.vector) / __norm(q.vector)


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
class SentimentWeightingModel(SentimentWeightingModelMixin, scoring.BM25F):
  def score_combination_function(self, content, sentiment):
    return linear_combination(content, sentiment)

  def vector_similarity_function(self, document, query):
    return cosine_similarity(document, query)