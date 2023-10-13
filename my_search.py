from whoosh.index import open_dir
from whoosh.fields import *
from whoosh import scoring, searching, matching, qparser

import sentiment

index = open_dir("indexdir")


class CosineSimilarity(scoring.WeightingModel):
  def scorer(self, searcher, fieldname, text, qf=1):
    return self.CosineSimilarityScorer()

  class CosineSimilarityScorer(scoring.BaseScorer):
    def score(self, matcher):
      return 1.0


def parse_query(schema, main_part, sentiment_part):
  # Main query should not contain sentiments as no results are returned otherwise
  # Use a plugin for the check, because operations are simpler
  parser = qparser.QueryParser("content", schema)
  parser.add_plugin(sentiment.query_parsing.NoSentimentPlugin())
  main_query = parser.parse(main_part)

  # If the sentiment part is not provided
  if not sentiment_part or not sentiment_part.strip():
    return main_query

  # Parse the sentiment query
  parser = qparser.QueryParser("sentiment", schema)
  parser.add_plugin(sentiment.query_parsing.SentimentParserPlugin())
  sentiment_query = parser.parse(sentiment_part)
  return sentiment.query_parsing.ContentWithSentimentQuery(main_query, sentiment_query)


query = parse_query(index.schema, "sample", "joy AND NOT fear")
with index.searcher(weighting=CosineSimilarity()) as searcher:
  for result in searcher.search(query):
    print(result)
