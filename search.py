import app.searching
import whoosh.index
import pynput.keyboard
import itertools

class SearchViewer:
  def __init__(self, main_query, sentiment_query, index_directory):
    self.main_query = main_query
    self.sentiment_query = sentiment_query
    self.searcher = app.searching.SearchEngine()
    self.searcher.set_index(whoosh.index.open_dir(index_directory))
    self.result_rank = 1
    self.result = None

  def output_result(self):
    results = self.searcher.search(self.main_query, self.sentiment_query, limit=self.result_rank)
    results = itertools.islice(results, self.result_rank - 1, self.result_rank)

    for result in results:
      print("\n" * 10)
      print(f"Score: {result.score:.2f}")
      print(f"Sentiment: {result['sentiment'].human_readable(0.1)}")
      print(f"Show: {result['title']} - Episode {result['episode']}")
      print("-"*20)
      print(result['content'])
      print("-"*20)
      print(f"Rank {self.result_rank}")
      print("A for previous result - D for next result - CTRL+C to exit")
      return True
    return False
  
  def next_result(self):
    self.result_rank += 1
    if not self.output_result():
      self.result_rank -= 1
      print("No results left!")

  def prev_result(self):
    if self.result_rank <= 1:
      print("This is already the first result!")
      return
    
    self.result_rank = self.result_rank - 1
    self.output_result()

  def run(self):
    if not self.output_result():
      print("No results!")
      return
    
    try:
      h = pynput.keyboard.GlobalHotKeys({
        'd': lambda: self.next_result(),
        'a': lambda: self.prev_result(),
        '<ctrl>+c': lambda: h.stop(),
      })
      with h:
        h.join()
    except KeyboardInterrupt:
      pass


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('index_directory')
  parser.add_argument('main_query')
  parser.add_argument('sentiment_query', nargs='?', default=None)

  args = parser.parse_args()

  viewer = SearchViewer(args.main_query, args.sentiment_query, args.index_directory)
  exit(viewer.run())
