
import praw
import markdown
from praw.models import MoreComments
import reddit.filtering
import os
import whoosh.index
import sentiment.sentiment_analysis
import sentiment.schema
import numpy as np
import reddit.parsing
#from sentiment import sentiment_analysis

index_dir = "indexdir"
if not os.path.exists(index_dir):
  os.mkdir(index_dir)

# Create or open the index
index = whoosh.index.create_in(index_dir, sentiment.schema.SCHEMA)

red = praw.Reddit(
  client_id="fyFBUMdaXtoogBzfHs-FQg",
  client_secret="1Wkzf7IRXGgHnd_HScgPpFJUwc6IZg",
  password="thequickbrownfoxjumpsoverthelazydog",
  user_agent="unimore-ir-sentiment-analysis",
  username="Extension_Pudding570",
)
ep_bot = red.redditor("AutoLovepon")

url = "https://www.reddit.com/r/anime/comments/17a55ep/helck_episode_15_discussion/"
submission = red.submission(url=url)
titolo,episodio=reddit.parsing.parse_post_title(submission.title)
"""
filtrare pagine url tipo https//image
filtrare gli a capo che vengono messi come /n
filtrare caratteri speciali generati 
gestione parole in grasetto

titolo
id

"""

for top_level_comment in submission.comments[1:]:
  if isinstance(top_level_comment, MoreComments):
    continue
  if top_level_comment.body =='[removed]' or top_level_comment.body == '[deleted]':
    continue
  content=reddit.filtering.markdown_to_plaintext(top_level_comment.body)
  with index.writer() as writer:
    writer.add_document(
      content=content,
      sentiment=sentiment.sentiment_analysis.classify_text(content)[0],
      title=titolo,
      episode=episodio,
      comment_id=top_level_comment.id
    )
    print(top_level_comment.id)
