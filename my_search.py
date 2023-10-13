from whoosh.index import open_dir
from whoosh.fields import *
from whoosh import qparser, scoring
import sentiment



def parse_query(schema, main_part, sentiment_part=None):
  # Main query should not contain sentiments as no results are returned otherwise
  # Use a plugin for the check, because operations are simpler
  parser = qparser.QueryParser("content", schema)
  parser.add_plugin(sentiment.query_parsing.NoSentimentPlugin())
  main_query = parser.parse(main_part)

  # If the sentiment part is not provided
  if not sentiment_part or not sentiment_part.strip():
    return (main_query, None)

  # Parse the sentiment query
  parser = qparser.QueryParser("sentiment", schema)
  parser.add_plugin(sentiment.query_parsing.SentimentParserPlugin())
  sentiment_query = parser.parse(sentiment_part)
  return (main_query, sentiment_query.sentiment_vector)


index = open_dir("indexdir")
query, sentiment_vector = parse_query(index.schema, "sample", "joy AND NOT fear")
weighting_model = sentiment.sentiment_scoring.make_sentiment_weighting_mdl_class(scoring.BM25F)()

with index.searcher(weighting=weighting_model) as searcher:
  weighting_model.set_query_sentiment_vector(sentiment_vector)
  for result in searcher.search(query):
    print(result)
