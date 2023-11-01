from whoosh import fields, analysis, formats, reading, writing

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


SCHEMA_V1 = fields.Schema(
  content=fields.TEXT(stored=True),
  sentiment=SentimentField(),
  title=fields.TEXT(stored=True),
  episode=fields.NUMERIC(stored=True),
  comment_id=fields.ID(stored=True, unique=True),
  submission_id=fields.ID(stored=True, unique=True)
)

# Changed analyzer for content
SCHEMA_V2 = fields.Schema(
  content=fields.TEXT(stored=True, analyzer=analysis.LanguageAnalyzer('en')),
  sentiment=SentimentField(),
  title=fields.TEXT(stored=True, analyzer=analysis.RegexTokenizer()),
  episode=fields.NUMERIC(stored=True),
  comment_id=fields.ID(stored=True, unique=True),
  submission_id=fields.ID(stored=True, unique=True)
)

# Changed analyzer for title
SCHEMA_V3 = fields.Schema(
  content=fields.TEXT(stored=True, analyzer=analysis.LanguageAnalyzer('en')),
  sentiment=SentimentField(),
  title=fields.TEXT(stored=True, analyzer=analysis.SimpleAnalyzer()),
  episode=fields.NUMERIC(stored=True),
  comment_id=fields.ID(stored=True, unique=True),
  submission_id=fields.ID(stored=True, unique=True)
)

SCHEMA = SCHEMA_V3

def schema_update_just_copy(index_from: reading.IndexReader, index_to: writing.IndexWriter):
  # Just need to run the analyzer - copy everything
  for _, stored in index_from.iter_docs():
    index_to.add_document(**stored) 