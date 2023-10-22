import asyncio
import logging
import sentiment.sentiment_analysis
import whoosh.index

logger = logging.getLogger(__name__)

async def process_comment_chunk(comment_chunk, index, index_writer):
  logger.info("Processing chunk of %d comments.", len(comment_chunk))
  
  # Perform sentiment analysis on the whole chunk of comments in a single request
  sentiments = await sentiment.sentiment_analysis.classify_text([comment['content'] for comment in comment_chunk])
  for comment, sentiment_vector in zip(comment_chunk, sentiments):
    comment['sentiment'] = sentiment_vector

    index_writer.add_document(**comment)
    logger.debug(comment)

class CommentConsumer:
  def __init__(self, index: whoosh.index.Index, queue: asyncio.Queue, chunk_size):
    self.queue = queue
    self.chunk_size = chunk_size
    self.index = index

  async def run(self):
    logger.info("Running.")

    with self.index.writer() as index_writer:
      try:
        while True:
          # Read from the queue until we have enough comments
          chunk = []
          while len(chunk) < self.chunk_size:
            chunk.append(await self.queue.get())
          
          # Process the chunk of comments
          await process_comment_chunk(chunk, self.index, index_writer)
      except asyncio.CancelledError:
        pass

    logger.info("Exiting.")