import praw
from praw.models import MoreComments
import reddit.filtering
import os
import whoosh.index
import sentiment.sentiment_analysis
import sentiment.schema
import reddit.parsing
import reddit.filtering
from common_utils.chunk import chunk
import logging


logger = logging.getLogger(__name__)


def store_single_submission(submission, index_writer = None, chunk_size=100000):
  title_parse_result = reddit.parsing.parse_post_title(submission.title)
  if title_parse_result is None:
    logger.warning("Skipping post due to bad title: %s", submission.title)
    return
  title, episode = title_parse_result
  logger.info("Processing submission: %s - Episode %d.", title, episode)

  comments = submission.comments[1:]

  # TODO: replace MoreComments instead of just removing them
  # Filter out MoreComments
  comments = filter(lambda comment: not isinstance(comment, MoreComments), comments)

  # Parse the comments without performing sentiment analysis
  comments = ({
      'content': reddit.parsing.markdown_to_plaintext(comment.body),
      'title': title,
      'episode': episode,
      'comment_id': comment.id
   }
   for comment in comments
  )

  # Apply the comment filter
  comments = filter(reddit.filtering.filter_comment, comments)

  # Process the comments in chunks
  for comment_chunk in chunk(comments, chunk_size):
    logger.debug("Processing comment chunk of size %d.", len(comment_chunk))
    
    # Perform sentiment analysis on the whole chunk of comments in a single request
    sentiments = sentiment.sentiment_analysis.classify_text([comment['content'] for comment in comment_chunk])
    
    for comment, sentiment_vector in zip(comment_chunk, sentiments):
      comment['sentiment'] = sentiment_vector
      logger.debug(comment)
      if index_writer:
        index_writer.add_document(**comment)


def index_creator(index_directory, simulate):
  red = praw.Reddit(
    client_id="fyFBUMdaXtoogBzfHs-FQg",
    client_secret="1Wkzf7IRXGgHnd_HScgPpFJUwc6IZg",
    password="thequickbrownfoxjumpsoverthelazydog",
    user_agent="unimore-ir-sentiment-analysis",
    username="Extension_Pudding570",
  )

  ep_bot = red.redditor("AutoLovepon")
  submissions = ep_bot.submissions.top(limit=None)

  def process_submissions(index_writer):
    logger.info("Processing submissions.")
    for submission in submissions:
      store_single_submission(submission, index_writer)

  if simulate:
    logger.warning("RUNNING IN SIMULATION MODE")
    process_submissions(None)

  else:
    # Open the index
    if not os.path.exists(index_directory):
      logger.info("Creating a new index...")
      os.mkdir(index_directory)
      index = whoosh.index.create_in(index_directory, sentiment.schema.SCHEMA)
    else:
      logger.info("Opening pre-existing index...")
      index = whoosh.index.open_dir(index_directory)

    # Create the writer and process submissions
    with index.writer() as index_writer:
      process_submissions(index_writer)
    

import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("index_directory", help="The directory in which the index will be created / updated.")
  parser.add_argument("-s", "--simulate", action='store_true', help="If specified, the script will just open/create the index, and not actually write documents in it.")
  args = parser.parse_args()

  logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', filename='index_creator.log', encoding='utf-8', level=logging.WARNING)

  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
  console.setFormatter(formatter)
  logging.getLogger('').addHandler(console)

  logger.setLevel(logging.DEBUG)
  logging.getLogger('huggingface').setLevel(logging.DEBUG)

  index_creator(args.index_directory, args.simulate)
  return 0

if __name__ == '__main__':  
  exit(main())