import os
import whoosh.index
import sentiment


index_dir = "indexdir"
if not os.path.exists(index_dir):
  os.mkdir(index_dir)

# Create or open the index
index = whoosh.index.create_in(index_dir, sentiment.schema.SCHEMA)

import numpy as np
# Create an AsyncWriter to add documents to the index
with index.writer() as writer:
  writer.add_document(
    content="We are doomed",
    sentiment=sentiment.SentimentVector(np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])),
    title="Cyka blyat",
    episode=69,
    post_id='177h3tj',
    comment_id='k4tatec'
  )