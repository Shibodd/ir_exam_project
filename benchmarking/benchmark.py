from .benchmark_spec import BenchmarkQuerySpec
from . import dcg
from app.searching import SearchEngine
import itertools
import numpy as np

def benchmark(engine: SearchEngine, benchmark_spec: list[BenchmarkQuerySpec]):
  # For a benchmark, we have to allow hits only of documents present in the benchmark dataset
  # Just query on the main index with a huge query filtering on comment ids, for example:
  # content:(character development) AND comment_id:(fk919f OR 1k9fjs OR lla01l OR 10k10e OR ...)

  def build_comment_query(comment_ids):
    return f'comment_id:({" OR ".join(comment_ids)})'

  def build_main_query(main_query, comment_ids):
    return f'({main_query}) AND {build_comment_query(comment_ids)}'


  # Make sure that all comments required by the benchmark are present in the index first, to prevent wrong results
  print("Checking that all documents in the benchmark dataset are in the index...")
  benchmark_comment_ids = set(itertools.chain.from_iterable(query_spec.dataset.keys() for query_spec in benchmark_spec))
  present_comment_ids = set(result['comment_id'] for result in engine.search(build_comment_query(benchmark_comment_ids)))
  if benchmark_comment_ids != present_comment_ids:
    # TODO: Download missing comments from reddit
    raise NotImplementedError("TODO: Download missing comments from reddit")
  

  print("Benchmarking...")

  ndcg_by_query = []
  for i, query_spec in enumerate(benchmark_spec):
    print(f"Query {i + 1} of {len(benchmark_spec)}: content:'{query_spec.main_query}', sentiment:'{query_spec.sentiment_query}'")
    main_query = build_main_query(query_spec.main_query, query_spec.dataset.keys())

    results = engine.search(main_query, query_spec.sentiment_query)

    # For each result, get the comment id and lookup its relevance to the current query in the benchmark dataset
    relevances = np.fromiter((query_spec.dataset[result['comment_id']] for result in results), dtype=int)

    assert len(relevances) <= len(query_spec.dataset), "The search contains more results than the dataset."

    ndcg = dcg.compute_NDCG(relevances, query_spec)
    print("NDCG for this query:", ndcg)
    ndcg_by_query.append(ndcg)

  print("== Average NDCG:", dcg.compute_average_NDCG(ndcg_by_query, benchmark_spec))

  return ndcg_by_query