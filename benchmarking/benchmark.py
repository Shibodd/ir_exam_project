from .benchmark_spec import BenchmarkQuerySpec
from . import dcg
from app.searching import SearchEngine
import whoosh.index
import logging

logger = logging.getLogger(__name__)

def benchmark(engine: SearchEngine, benchmark_spec: list[BenchmarkQuerySpec]):
  print("Benchmarking...")

  ndcg_by_query = []
  for i, query_spec in enumerate(benchmark_spec):
    print(f"Query {i + 1} of {len(benchmark_spec)}: content:'{query_spec.main_query}', sentiment:'{query_spec.sentiment_query}'")

    index = whoosh.index.open_dir(query_spec.index_dir)
    engine.set_index(index)

    results = engine.search(query_spec.main_query, query_spec.sentiment_query)
    relevances = [result['relevance'] for result in results]

    ndcg = dcg.compute_NDCG(relevances, query_spec)
    print("NDCG for this query:", ndcg)
    ndcg_by_query.append(ndcg)

  print("== Average NDCG:", dcg.compute_average_NDCG(ndcg_by_query, benchmark_spec))

  return ndcg_by_query