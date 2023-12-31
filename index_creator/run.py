import index_creator
import asyncio
import logging

import logging
import os
import sentiment.schema
import whoosh.index
import asyncpraw

logger = logging.getLogger(__name__)

async def run(red: asyncpraw.Reddit, index_directory, submission_ids: list[str], chunk_size=1000, all_comments=False):
  if not os.path.exists(index_directory):
    logger.info("Creating a new index...")
    os.mkdir(index_directory)
    index = whoosh.index.create_in(index_directory, sentiment.schema.SCHEMA)
  else:
    logger.info("Opening pre-existing index...")
    index = whoosh.index.open_dir(index_directory)
  
  logger.info("Starting")
  queue = asyncio.Queue(2 * chunk_size)
  with index_creator.IndexManager(index) as index_manager:
    task1 = asyncio.create_task(index_creator.CommentProducer(index_manager, queue).run(red, submission_ids, all_comments))
    task2 = asyncio.create_task(index_creator.CommentConsumer(index_manager, queue, chunk_size).run())
    
    # The tasks handle cancellation gracefully
    while True:
      try:
        await asyncio.gather(task1)
        task2.cancel()
        await asyncio.gather(task2) 
        return
      except asyncio.CancelledError:
        pass