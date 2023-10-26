import pathlib
import whoosh.index
import app
import benchmarking

import common_utils.arrays
import numpy as np


def visualize_single_query_results(dcg: np.ndarray, idcg_lb: np.ndarray):
  print(dcg, idcg_lb)

def visualize_average_results(dcg: np.ndarray, idcg_lb: np.ndarray):
  print(dcg, idcg_lb)


def run_interactive_benchmark_query(searcher: app.SearchEngine, bqm: benchmarking.BenchmarkQueryManager, limit=50):
  """
  Returns the score for each comment in the query results.
  If the comment was not previously scored, prompts the user to score the result.
  """

  # Score vector in order of ranking (leftmost is the top result)
  scores = [2, 1, 2, 0, 0, 2, 0]
  
  for result in searcher.search(bqm.main_query, bqm.sentiment_query):
    """
    TODO:
    Se il commento ha gia' un punteggio, usare quello senza mostrare output;
    altrimenti chiedere all'utente un punteggio da 0 a 2 (non rilevante, poco rilevante, rilevante)
    mostrandogli il commento, poi usa quel punteggio e salvalo
    """

    # Puoi prendere i campi dello schema dal risultato:
    # result['comment_id']
    # result['content']
    
    # Per scrivere o leggere i punteggi:
    # bqm.update_score(..)
    # bqm.get_score(..)
    # Il salvataggio e' gia' gestito dal context manager in run_interactive_benchmark
    pass

  return scores

def run_interactive_benchmark(index_dir, benchmark_dir):
  index_dir = pathlib.Path(index_dir)
  benchmark_dir = pathlib.Path(benchmark_dir)

  index = whoosh.index.open_dir(str(index_dir), readonly=True)
  searcher = app.SearchEngine()
  searcher.set_index(index)

  dcg_by_query = []
  idcg_lb_by_query = []

  for query_file in benchmark_dir.glob('*.json'):
    with benchmarking.BenchmarkQueryManager(query_file) as bqm:
      # The relevance score of each result
      scores = run_interactive_benchmark_query(searcher, bqm)

      # Lower bound for the Ideal DCG for this query
      # (it's very likely that we didn't rate all relevant documents!)
      query_idcg_lb = benchmarking.dcg.compute_ideal_DCG(bqm.iter_scores())
    
    # Discounted Cumulative Gain for this query
    query_dcg = benchmarking.dcg.compute_DCG(scores)

    dcg_by_query.append(query_dcg)
    idcg_lb_by_query.append(query_idcg_lb)
    
    # TODO: Fare un output decente per mostrare i risultati
    visualize_single_query_results(query_dcg, query_idcg_lb)

  # Compute the average DCG and IDCG lower bound over all the queries of this benchmark
  average_dcg = common_utils.arrays.average(dcg_by_query)
  average_idcg_lb = common_utils.arrays.average(idcg_lb_by_query)

  visualize_average_results(average_dcg, average_idcg_lb)

  

import argparse
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('index_dir')
  parser.add_argument('benchmark_dir')
  args = parser.parse_args()

  run_interactive_benchmark(args.index_dir, args.benchmark_dir)

  return 0

if __name__ == '__main__':
  exit(main())