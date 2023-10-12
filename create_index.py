import os
from whoosh.index import create_in
from whoosh import fields
import sentiment

schema = fields.Schema(
  content=fields.TEXT(),
  emotion=sentiment.schema.SentimentField()
)

index_dir = "indexdir"
if not os.path.exists(index_dir):
  os.mkdir(index_dir)

# Create or open the index
index = create_in(index_dir, schema)

# Create an AsyncWriter to add documents to the index
with index.writer() as writer:
  writer.add_document(content="This is a sample document.", emotion=sentiment.SentimentVector([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]))