import asyncio
import index_creator.run
import logging
import asyncpraw

logger = logging.getLogger(__name__)

async def add_submission_to_index(index_directory, submission_id, all_comments=False):
  logger.info("Connecting to Reddit...")
  async with asyncpraw.Reddit(
      client_id="fyFBUMdaXtoogBzfHs-FQg",
      client_secret="1Wkzf7IRXGgHnd_HScgPpFJUwc6IZg",
      password="thequickbrownfoxjumpsoverthelazydog",
      user_agent="unimore-ir-sentiment-analysis",
      username="Extension_Pudding570",
    ) as red:

    submission_ids = [submission_id]
    await index_creator.run.run(red, index_directory, submission_ids, all_comments=all_comments)

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('index_directory')
  parser.add_argument('submission_id')
  parser.add_argument('--all_comments', action='store_true')
  args = parser.parse_args()

  logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', filename='add_submission.log', encoding='utf-8', level=logging.WARNING)

  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
  console.setFormatter(formatter)
  logging.getLogger('').addHandler(console)

  logger.setLevel(logging.DEBUG)
  logging.getLogger('huggingface').setLevel(logging.DEBUG)
  logging.getLogger('index_creator').setLevel(logging.DEBUG)
  logging.getLogger(__name__).setLevel(logging.DEBUG)
  logging.getLogger('').setLevel(logging.DEBUG)

  try:
    exit(asyncio.run(add_submission_to_index(args.index_directory, args.submission_id, args.all_comments)))
  except KeyboardInterrupt:
    exit(0)
