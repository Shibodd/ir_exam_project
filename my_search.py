from app.searching import SearchEngine
from whoosh.index import open_dir

index = open_dir("indexdir")
searcher = SearchEngine(index)
for result in searcher.search('title:"Cyka blyat" episode:69', 'fear'):
  print(result)