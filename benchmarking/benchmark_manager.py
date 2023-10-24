import json
import pathlib
import shutil

""" 
// Example query
{
  "main_query": "Gesu' cristo",
  "sentiment_query": "disgust AND anger",
  "relevances": {
    "iw12da": 3,
    "ab244f": 1,
    "c1364e": 0,
    "flh054": 3,
  }
}
"""

class BenchmarkQueryManager:
  def __init__(self, path, main_query=None, sentiment_query=None):
    self.main_query = main_query
    self.sentiment_query = sentiment_query
    self.path = path
    self.__relevances = {}

  # Context manager
  def __enter__(self):
    self.load()

  def __exit__(self, *exc_args):
    self.save()

  # File management
  def load(self):
    """ Discards any changes and reloads the query from file. """
    if self.__path.is_file():
      with self.__path.open('rt', encoding='utf-8') as f:
        data = json.load(f)
        
      self.main_query = data['main_query'],
      self.sentiment_query = data['sentiment_query'],
      self.__relevances = data['relevances']
    else:
      self.main_query = ''
      self.sentiment_query = ''
      self.__relevances = {}
  
  def save(self):
    """ Commits any change to file. """
    use_backup = self.__path.is_file()
    if use_backup:
      bak = pathlib.Path(self.__path).with_suffix(".bak")
      shutil.copy(str(self.__path), str(bak))
    
    with self.__path.open('wt', encoding='utf-8') as f:
      json.dump({
        'main_query': self.main_query,
        'sentiment_query': self.sentiment_query,
        'relevances': self.__relevances
      }, f)

    if use_backup:
      bak.unlink()

  @property
  def path(self):
    return self.__path
  
  @property.setter
  def path(self, value):
    self.__path = pathlib.Path(value)

  def is_comment_scored(self, comment_id):
    return comment_id in self.__relevances

  def get_score(self, comment_id):
    return self.__relevances.get(comment_id, None)

  def update_score(self, comment_id, new_score):
    self.__relevances[comment_id] = new_score