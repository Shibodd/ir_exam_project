import sentiment
from app.query_parsing import parse_query

class SearchEngine:
  def __init__(self, index, weighting_model=sentiment.sentiment_scoring.SentimentWeightingModel()):
    self.index = index
    self.weighting_model = weighting_model

  def search(self, main_query, sentiment_query = None):
    query, sentiment_vector = parse_query(self.index.schema, main_query, sentiment_query)

    with self.index.searcher(weighting=self.weighting_model) as searcher:
      self.weighting_model.set_query_sentiment_vector(sentiment_vector)
      for result in searcher.search(query):
        yield result