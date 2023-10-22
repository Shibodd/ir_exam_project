import praw
from praw.models import MoreComments
import os
import whoosh.index
import sentiment.sentiment_analysis
import sentiment.schema
import reddit.parsing
import reddit.filtering

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

for top_level_comment in submission.comments[1:]:
  if isinstance(top_level_comment, MoreComments):
    continue

  if not reddit.filtering.filter_comment(top_level_comment.body):
    continue

  content = reddit.parsing.markdown_to_plaintext(top_level_comment.body)

  with index.writer() as writer:
    writer.add_document(
      content=content,
      sentiment=sentiment.sentiment_analysis.classify_text(content)[0],
      title=titolo,
      episode=episodio,
      comment_id=top_level_comment.id
    )
    print(top_level_comment.id)
