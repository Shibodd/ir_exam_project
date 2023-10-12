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


def parse_query(schema, main_part, emotion_part):
  # Main query should not contain emotions as no results are returned otherwise
  # Use a plugin for the check, because operations are simpler
  parser = qparser.QueryParser("content", schema)
  parser.add_plugin(sentiment.NoEmotionPlugin())
  main_query = parser.parse(main_part)

  # If the emotion part is not provided
  if not emotion_part or not emotion_part.strip():
    return main_query

  # Parse the emotion query
  parser = qparser.QueryParser("emotion", schema)
  emotion_query = parser.parse(emotion_part)
  return sentiment.EmotionQuery(main_query, emotion_query)


# Create a QueryParser
with index.searcher(weighting=CosineSimilarity()) as searcher:
  print(parse_query(index.schema, "sample terminal", "happy AND NOT sad"))
  exit()

  # Search for documents
  results = searcher.search(query)

  for result in results:
    print(result)
