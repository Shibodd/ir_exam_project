import asyncio
import logging
import sentiment.sentiment_analysis

from . import IndexManager

logger = logging.getLogger(__name__)

class CommentConsumer:
  def __init__(self, index_manager: IndexManager, queue: asyncio.Queue, chunk_size):
    self.queue = queue
    self.chunk_size = chunk_size
    self.index_manager = index_manager


  async def process_comment_chunk(self, comment_chunk):
    logger.info("Processing chunk of %d comments.", len(comment_chunk))
    
    # Perform sentiment analysis on the whole chunk of comments in a single request
    sentiments = await sentiment.sentiment_analysis.classify_text([comment['content'] for comment in comment_chunk])

    writer = self.index_manager.get_writer()
    for comment, sentiment_vector in zip(comment_chunk, sentiments):
      comment['sentiment'] = sentiment_vector
      writer.add_document(**comment)
      logger.debug(comment)
    


  async def run(self):
    logger.info("Running.")

    try:
      while True:
        # Read from the queue until we have enough comments
        chunk = []
        while len(chunk) < self.chunk_size:
          chunk.append(await self.queue.get())
        
        # Process the chunk of comments
        await self.process_comment_chunk(chunk)
    except asyncio.CancelledError:
      pass

    logger.info("Exiting.")