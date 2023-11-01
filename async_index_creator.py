import index_creator
import asyncio
import logging

import logging
import os
import sentiment.schema
import whoosh.index
import asyncpraw
import argparse
import reddit

logger = logging.getLogger(__name__)

async def run_index_creator(index_directory):
  if not os.path.exists(index_directory):
    logger.info("Creating a new index...")
    os.mkdir(index_directory)
    index = whoosh.index.create_in(index_directory, sentiment.schema.SCHEMA)
  else:
    logger.info("Opening pre-existing index...")
    index = whoosh.index.open_dir(index_directory)

  logger.info("Connecting to Reddit...")
  async with asyncpraw.Reddit(
      client_id="fyFBUMdaXtoogBzfHs-FQg",
      client_secret="1Wkzf7IRXGgHnd_HScgPpFJUwc6IZg",
      password="thequickbrownfoxjumpsoverthelazydog",
      user_agent="unimore-ir-sentiment-analysis",
      username="Extension_Pudding570",
    ) as red:

    logger.info("Downloading archive...")
    submission_ids = await reddit.submission_archive.get_submissions_for_years(red, [2022, 2021, 2020, 2019, 2018, 2017, 2016])

    logger.info("Starting")
    queue = asyncio.Queue(400)
    with index_creator.IndexManager(index) as index_manager:
      task1 = asyncio.create_task(index_creator.CommentProducer(index_manager, queue).run(red, submission_ids))
      task2 = asyncio.create_task(index_creator.CommentConsumer(index_manager, queue, 200).run())
      
      # The tasks handle cancellation gracefully
      while True:
        try:
          await asyncio.gather(task1)
          task2.cancel()
          await asyncio.gather(task2) 
          return
        except asyncio.CancelledError:
          pass


async def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("index_directory", help="The directory in which the index will be created / updated.")
  args = parser.parse_args()

  logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', filename='index_creator.log', encoding='utf-8', level=logging.WARNING)

  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
  console.setFormatter(formatter)
  logging.getLogger('').addHandler(console)

  logger.setLevel(logging.DEBUG)
  logging.getLogger('huggingface').setLevel(logging.DEBUG)
  logging.getLogger('index_creator').setLevel(logging.DEBUG)
  logging.getLogger('async_index_creator').setLevel(logging.DEBUG)
  logging.getLogger('').setLevel(logging.DEBUG)

  await run_index_creator(args.index_directory)
  return 0


if __name__ == '__main__':
  try:
    exit(asyncio.run(main()))
  except KeyboardInterrupt:
    exit(0)