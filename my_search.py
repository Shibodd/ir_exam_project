from app.searching import SearchEngine
import whoosh.index

searcher = SearchEngine()
searcher.set_index(whoosh.index.open_dir("indexdir"))
for result in searcher.search('title:"Cyka blyat" episode:69', 'fear'):
  print(result)