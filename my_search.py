from app.searching import SearchEngine
import whoosh.index

searcher = SearchEngine()
searcher.set_index(whoosh.index.open_dir("indexdir"))
for result in searcher.search('Azudra', 'sadness AND NOT surprise'):
  # print("\n\n\n")
  # print(result['content'])
  print(f"{result.score:.2f} {result['sentiment'].human_readable()}")