import argparse
import whoosh.index
import whoosh.searching
from common_utils.user_input import input_integer
from benchmarking.benchmark_spec import BenchmarkQuerySpec, parse_query_file
from app.searching import SearchEngine
from benchmarking.schema import SCHEMA


def comment_exists_in_index(index: whoosh.index.Index, comment_id: str):
  try:
    return index.reader().postings("comment_id", comment_id).is_active()
  except whoosh.searching.TermNotFound:
    return False


def query_index_creator(engine: SearchEngine, query_spec: BenchmarkQuerySpec):
  try:
    if query_spec.index_dir.is_dir():
      query_index = whoosh.index.open_dir(query_spec.index_dir)
    else:
      query_spec.index_dir.mkdir()
      query_index = whoosh.index.create_in(query_spec.index_dir, SCHEMA)

    results = engine.search(query_spec.main_query, query_spec.sentiment_query)
    total = 0
    already_rated = 0
    rated_now = 0
    for result in results:
      total += 1
      if comment_exists_in_index(query_index, result['comment_id']):
        already_rated += 1
        continue

      print("\n" * 5)
      print("  content:", query_spec.main_query)
      print("sentiment:", query_spec.sentiment_query)
      print(f"==== Comment {result['comment_id']}")
      print(result['content'])
      relevance = input_integer("==== Enter relevance: ", 0, 3)
      with query_index.writer() as writer:
        writer.add_document(**result, relevance=relevance)
      rated_now += 1
    print("No documents left!")
  except KeyboardInterrupt:
    print("Exiting.")
  finally:
    print("\nStats for this query:")
    print(f"{total} results in main index")
    print(f"{already_rated} documents pre-existing in the dataset")
    print(f"{rated_now} documents rated in this session.")
  
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("main_index_dir")
  parser.add_argument("query_file")
  args = parser.parse_args()

  index = whoosh.index.open_dir(args.main_index_dir)
  query_spec = parse_query_file(args.query_file)

  engine = SearchEngine()
  engine.set_index(index)

  query_index_creator(engine, query_spec)

  return 0

if __name__ == '__main__':  
  exit(main())