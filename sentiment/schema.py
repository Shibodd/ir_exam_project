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


SCHEMA = fields.Schema(
  content=fields.TEXT(),
  sentiment=SentimentField(),
  title=fields.TEXT(stored=True),
  episode=fields.NUMERIC(stored=True),
  post_id=fields.ID(stored=True),
  comment_id=fields.ID(stored=True),
)