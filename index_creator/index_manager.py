import whoosh.index
import whoosh.writing
import whoosh.searching
import logging


logger = logging.getLogger(__name__)


class IndexManager:
  __searcher: whoosh.searching.Searcher
  __writer: whoosh.writing.IndexWriter

  def __init__(self, index: whoosh.index.Index):
    self.__index = index
    self.__mode = None

  def __enter__(self):
    return self

  def __exit__(self, exc_type, *exc_args):
    self.release(exc_type)

  def release(self, exc_type):
    """ Releases the resources used for the current mode. """
    if self.__mode == 'w':
      logger.debug('Releasing writer.')
      self.__writer.__exit__(exc_type, None, None)
    if self.__mode == 'r':
      logger.debug('Releasing searcher.')
      self.__searcher.__exit__(exc_type, None, None)

    self.__mode = None

  def __acquire_mode(self, mode: str):
    if self.__mode != mode:
      self.release(None)
      self.__mode = mode
      return True
    return False

  def get_writer(self):
    if self.__acquire_mode('w'):
      logger.debug('Creating writer.')
      self.__writer = self.__index.writer()
    return self.__writer
  
  def get_searcher(self):
    if self.__acquire_mode('r'):
      logger.debug('Creating searcher.')
      self.__searcher = self.__index.searcher()
    return self.__searcher