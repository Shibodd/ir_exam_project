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
    logger.info("Calling Inference API with %d comments...", len(comment_chunk))
    
    # Perform sentiment analysis on the whole chunk of comments in a single request
    sentiments = await sentiment.sentiment_analysis.classify_text([comment['content'] for comment in comment_chunk])

    logger.info("Writing %d comments to the index...", len(comment_chunk))
    
    writer = self.index_manager.get_writer()
    for comment, sentiment_vector in zip(comment_chunk, sentiments):
      comment['sentiment'] = sentiment_vector
      writer.add_document(**comment)
      logger.debug(comment)
      
    logger.info("Done writing %d comments.", len(comment_chunk))
    

  async def run(self):
    logger.info("Running.")
    
    processing = False
    chunk = []

    try:
      while True:
        # Read from the queue until we have enough comments
        chunk.clear()
        while len(chunk) < self.chunk_size:
          chunk.append(await self.queue.get())
        
        # Process the chunk of comments
        processing = True # Avoid duplicates - prefer losing data
        await self.process_comment_chunk(chunk)
        processing = False

    except asyncio.CancelledError:
      # If we're being cancelled, first process the pending data.
      # If we were processing the data when CancelledError was raised, lose the data instead of writing duplicates.
      if len(chunk) > 0 and not processing:
        await self.process_comment_chunk(chunk)

    logger.info("Exiting.")