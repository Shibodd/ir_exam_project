import argparse
from whoosh.index import Index, open_dir as open_index_dir
from benchmarking.benchmark_spec import BenchmarkQuerySpec, parse_query_file
from app.searching import SearchEngine

def comment_exists_in_index(index: Index, comment_id: str):
  return index.reader().postings("comment_id", comment_id).is_active()

def query_index_creator(engine: SearchEngine, query_spec: BenchmarkQuerySpec):
  query_index = open_index_dir(query_spec.index_dir)
  results = engine.search(query_spec.main_query, query_spec.sentiment_query)
  for result in results:
    if comment_exists_in_index(query_index, result['comment_id']):
      continue
    
    relevance = input(f"Please evaluate the following comment.\n{result['content']}\nEnter relevance [0-3]:")


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("main_index_dir")
  parser.add_argument("query_file")
  args = parser.parse_args()

  index = open_index_dir(args.main_index_dir)
  query_spec = parse_query_file(args.query_file)

  engine = SearchEngine()
  engine.set_index(index)
  query_index_creator(engine, query_spec)
  return 0

if __name__ == '__main__':  
  exit(main())