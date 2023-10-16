import argparse
from whoosh.index import Index, open_dir as open_index_dir
from benchmarking.benchmark_spec import BenchmarkQuerySpec, parse_query_file

def comment_exists_in_index(index: Index, comment_id: str):
  return index.reader().postings("comment_id", comment_id).is_active()

def query_index_creator(main_index: Index, query_spec: BenchmarkQuerySpec):
  query_index = open_index_dir(query_spec.index_dir)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("main_index_dir")
  parser.add_argument("query_file")
  args = parser.parse_args()

  index = open_index_dir(args.main_index_dir)
  query_spec = parse_query_file(args.query_file)
  query_index_creator(index, query_spec)
  return 0

if __name__ == '__main__':  
  exit(main())