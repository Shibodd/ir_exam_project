import math
from whoosh import qparser
from whoosh.query import qcore

from . import SentimentVector
import functools

class NoSentimentPlugin(qparser.Plugin):
  """
  Raises an exception if a WordNode with fieldname sentiment is found in the AST.
  """

  def taggers(self, parser):
    return tuple()
  
  def filters(self, parser):
    # Absurdly high priority, hoping that this runs as the last plugin
    return [(self.raise_on_sentiment, math.inf)]
  
  def raise_on_sentiment(self, parser, group: qparser.GroupNode):  
    for node in group:
      if isinstance(node, qparser.GroupNode):
        self.raise_on_sentiment(parser, node)
      
      elif isinstance(node, qparser.WordNode) and node.fieldname == 'sentiment':
        raise qparser.QueryParserError("The sentiment field is not allowed in the main query.")

    return group
    

class SentimentParserPlugin(qparser.Plugin):
  """
  Compiles the sentiment expression's AST into a single sentiment node.
  """
  def taggers(self, parser):
    return tuple()
  
  def filters(self, parser):
    return [(self.parse_sentiments, math.inf)]
  
  def parse_sentiments(self, parser, group: qparser.GroupNode):
    return SentimentNode(self.__parse_sentiment_vector(group))

  def __parse_sentiment_vector(self, node: qparser.GroupNode):
    if isinstance(node, qparser.WordNode):
      if node.fieldname and node.fieldname != 'sentiment':
        raise qparser.QueryParserError(f"Only the sentiment field is allowed in a sentiment query, but found {node.fieldname}.")
      return SentimentVector(node.text)
    
    if isinstance(node, qparser.NotGroup):
      return ~self.__parse_sentiment_vector(node[0])
    
    if isinstance(node, qparser.AndGroup):
      reduce_fun = SentimentVector.__and__
    elif isinstance(node, qparser.OrGroup):
      reduce_fun = SentimentVector.__or__
    else:
      raise qparser.QueryParserError(f"Unsupported node type {type(node)}.")
    
    return functools.reduce(reduce_fun, (self.__parse_sentiment_vector(sub_node) for sub_node in node))


class SentimentNode(qparser.SyntaxNode):
  def __init__(self, sentiment_vector):
    self.sentiment_vector = sentiment_vector

  def query(self, parser):
    return SentimentQuery(self.sentiment_vector)
  

class SentimentQuery(qcore.Query):
  def __init__(self, sentiment_vector):
    self.sentiment_vector = sentiment_vector

  def __repr__(self):
    return f"{self.__class__.__name__}({self.sentiment_vector})"