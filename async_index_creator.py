import argparse
import index_creator.run
import asyncio
import logging

import logging
import asyncpraw

import reddit

logger = logging.getLogger(__name__)

async def run_index_creator(index_directory):
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
    await index_creator.run.run(red, index_directory, submission_ids)

if __name__ == '__main__':
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

  try:
    exit(asyncio.run(run_index_creator(args.index_directory)))
  except KeyboardInterrupt:
    exit(0)