from whoosh import fields, analysis, formats

class SentimentField(fields.FieldType):
  def __init__(self):
    self.analyzer = analysis.IDTokenizer()
    self.format = formats.Existence()

    self.stored = True
    self.scorable = True
    self.unique = False
    self.vector = False
    self.indexed = False
    self.set_sortable(False)