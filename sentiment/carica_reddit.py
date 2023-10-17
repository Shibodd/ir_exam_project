#import whoosh
import praw
from praw.models import MoreComments
#from sentiment import sentiment_analysis

reddit = praw.Reddit(
  client_id="fyFBUMdaXtoogBzfHs-FQg",
  client_secret="1Wkzf7IRXGgHnd_HScgPpFJUwc6IZg",
  password="thequickbrownfoxjumpsoverthelazydog",
  user_agent="unimore-ir-sentiment-analysis",
  username="Extension_Pudding570",
)
ep_bot = reddit.redditor("AutoLovepon")

url = "https://www.reddit.com/r/swordartonline/comments/15373ja/megathread_sword_art_online_alternative_gun_gale/"
submission = reddit.submission(url=url)
posts = []
for top_level_comment in submission.comments[1:]:
    if isinstance(top_level_comment, MoreComments):
        continue
    posts.append(top_level_comment.body)
posts = posts.columns=["body"]
indexNames = posts[(posts.body == '[removed]') | (posts.body == '[deleted]')].index
posts.drop(indexNames, inplace=True)
print(posts)
# Iterate over the bot posts
for submission in ep_bot.submissions.hot():
  print(f"Title :{submission.title}")
  print(f"Submission: {submission.name}")
  print(f"Submission: {submission.id}")
  # Iterate over the post comments
  for comment in submission.comments:
    # If the post was not deleted
    if comment.author is not None:
      print(f"Comment by {comment.author}")
      print(f"id :{comment}")

indexNames = posts[(posts.body == '[removed]') | (posts.body == '[deleted]')].index

posts.drop(indexNames, inplace=True)
