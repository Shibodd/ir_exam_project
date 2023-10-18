from app.searching import SearchEngine
import whoosh.index

searcher = SearchEngine()
searcher.set_index(whoosh.index.open_dir("indexdir"))
for result in searcher.search('Azudra'):
  print("\n\n\n")
  print(result['content'])
  print(result['sentiment'].human_readable())