import json
import pathlib
import shutil
import typing

class BenchmarkQueryManager:
  def __init__(self, path, main_query=None, sentiment_query=None):
    self.main_query = main_query
    self.sentiment_query = sentiment_query
    self.path = pathlib.Path(path)
    self.__relevances = {}

  # Context manager
  def __enter__(self):
    self.load()
    return self

  def __exit__(self, *exc_args):
    self.save()

  # File management
  def load(self):
    """ Discards any changes and reloads the query from file. """
    if self.__path.is_file():
      with self.__path.open('rt', encoding='utf-8') as f:
        data = json.load(f)
        
      self.main_query = data['main_query']
      self.sentiment_query = data['sentiment_query']
      self.__relevances = data.get('relevances', {})
    else:
      self.main_query = ''
      self.sentiment_query = ''
      self.__relevances = {}
  
  def save(self):
    """
    Commits any change to file. It will also create a backup file
    (same name as the output file, but with .bak extension)
    or overwrite it if it already exists. 
    """
    use_backup = self.__path.is_file()
    if use_backup:
      bak = pathlib.Path(self.__path).with_suffix(".bak")
      shutil.copy(str(self.__path), str(bak))
    
    with self.__path.open('wt', encoding='utf-8') as f:
      json.dump({
        'main_query': self.main_query,
        'sentiment_query': self.sentiment_query,
        'relevances': self.__relevances
      }, f, indent=2)

  @property
  def path(self):
    return self.__path
  
  @path.setter
  def path(self, value):
    self.__path = pathlib.Path(value)

  def get_score(self, comment_id: str) -> int:
    """ Returns the score of the comment with the specified id, or None if it was not scored."""
    return self.__relevances.get(comment_id, None)

  def update_score(self, comment_id: str, new_score: int) -> None:
    """ Updates the score of the comment with the specified id. """
    self.__relevances[comment_id] = new_score

  def iter_scored_comments(self) -> typing.Iterable[typing.Tuple[str, int]]:
    """ Returns all scored comments as an iterable of tuples (comment_id, score). """
    return self.__relevances.items()
  
  def iter_scores(self) -> typing.Iterable[int]:
    """ Returns an iterable over all scores. """
    return self.__relevances.values()