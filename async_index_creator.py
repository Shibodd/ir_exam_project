import index_creator
import asyncio
import logging

import logging
import os
import sentiment.schema
import whoosh.index


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', encoding='utf-8', level=logging.WARNING)
logging.getLogger('index_creator').setLevel(logging.DEBUG)
logging.getLogger('huggingface').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

index_directory = 'indexdir'

if not os.path.exists(index_directory):
  logger.info("Creating a new index...")
  os.mkdir(index_directory)
  index = whoosh.index.create_in(index_directory, sentiment.schema.SCHEMA)
else:
  logger.info("Opening pre-existing index...")
  index = whoosh.index.open_dir(index_directory)


async def main():
  queue = asyncio.Queue(400)

  with index_creator.IndexManager(index) as index_manager:
    task1 = asyncio.create_task(index_creator.CommentProducer(index_manager, queue).run())
    task2 = asyncio.create_task(index_creator.CommentConsumer(index_manager, queue, 200).run())

    while True:
      try:
        await asyncio.gather(task1, task2)
        return
      except asyncio.CancelledError:
        pass

try:
  asyncio.run(main())
except KeyboardInterrupt:
  pass