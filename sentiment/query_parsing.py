import math
from whoosh import qparser
from whoosh.query import qcore

from . import SentimentVector


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
        self.raise_on_sentiment_term(group)
      
      elif isinstance(node, qparser.WordNode) and node.fieldname == 'sentiment':
        raise Exception("Porcoddio cumpa', ti ho detto di non mettere emozioni uaa")

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
      if node.fieldname != 'sentiment':
        raise Exception("Ma porcamadonna. Qui ci vanno solo emozioni")
      return SentimentVector(node.text)
    
    ans = SentimentVector()
    if isinstance(node, qparser.AndGroup):
      v = self.__parse_sentiment_vector(node)
      for sub_node in node:


    else:
      pass

class SentimentNode(qparser.SyntaxNode):
  def __init__(self, vector):
    pass

  def query(self, parser):
    return super().query(parser)
  

class SentimentQuery(qcore.Query):
  def __init__(self, main_query, sentiment_vector):
    self.main_query = main_query
    self.sentiment_vector = sentiment_vector

  def __repr__(self):
    return f"{self.__class__.__name__}({self.main_query}, {self.sentiment_vector})"
  