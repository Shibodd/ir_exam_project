import asyncpraw
import asyncprawcore
import reddit.parsing
import logging
import reddit.filtering
import asyncio
from . import IndexManager
import reddit.submission_archive
import random

logger = logging.getLogger(__name__)


class CommentProducer:
  def __init__(self, index_manager: IndexManager, comment_queue: asyncio.Queue) -> None:
    self.index_manager = index_manager
    self.comment_queue = comment_queue

  async def __run_on_submission(self, submission: asyncpraw.reddit.models.Submission, title: str, episode: int):
    logger.info("Processing submission: '%s' - Episode %d.", title, episode)
    await submission.load()

    comments = submission.comments
    comments = filter(lambda comment: not isinstance(comment, asyncpraw.reddit.models.MoreComments), comments)
    comments = ({
        'content': reddit.parsing.markdown_to_plaintext(comment.body),
        'title': title,
        'episode': episode,
        'comment_id': comment.id,
        'submission_id': submission.id
      }
      for comment in comments
    )

    comments = filter(
      lambda comment: reddit.filtering.filter_comment(comment) and self.index_manager.get_searcher().document_number(comment_id=comment['comment_id']) is None,
      comments
    )
    
    for comment in comments:
      logger.debug("Put comment '%s'.", comment['comment_id'])
      await self.comment_queue.put(comment)


  async def __run(self, red: asyncpraw.Reddit, submission_ids: list[str]):
    logger.info("Processing submissions.")
    for submission_id in submission_ids:
      try:
        submission = await red.submission(submission_id)
      except Exception as e:
        logger.exception(e)
        continue

      title_parse_result = reddit.parsing.parse_post_title(submission.title)

      if title_parse_result is None:
        logger.warning("Skipping submission '%s' due to bad title.", submission.title)
        continue

      if self.index_manager.get_searcher().document_number(submission_id=submission.id):
        logger.warning("Skipping submission '%s' because at least one of its comments is already in the index.", submission.title)
        continue

      title, episode = title_parse_result
      try:
        await self.__run_on_submission(submission, title, episode)
      except Exception as e:
        logger.exception(e)
        continue


  async def run(self, red: asyncpraw.Reddit, submission_ids: list[str]):
    logger.info("Running.")
    try:
      await self.__run(red, submission_ids)
    except asyncio.CancelledError:
      pass
    logger.info("Exiting.")