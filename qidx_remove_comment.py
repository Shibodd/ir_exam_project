import argparse
from whoosh.index import open_dir as open_index_dir
from benchmarking.benchmark_spec import BenchmarkQuerySpec, parse_query_file

def remove_comment_from_query_index(query_spec: BenchmarkQuerySpec, comment_id: str):
  query_index = open_index_dir(query_spec.index_dir)
  query_index.delete_by_term("comment_id", comment_id)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("query_file")
  parser.add_argument("comment_id")
  args = parser.parse_args()

  query_spec = parse_query_file(args.query_file)
  remove_comment_from_query_index(query_spec, args.comment_id)
  return 0

if __name__ == '__main__':  
  exit(main())