import app
import benchmarking
import benchmarking.results
import common_utils.arrays
import pathlib
import whoosh.index
import common_utils.controllo_interi

def run_single_query(searcher: app.SearchEngine, bqm: benchmarking.BenchmarkQueryManager, limit=30):
  """
  Returns the score for each comment in the query results.
  If the comment was not previously scored, prompts the user to score the result.
  """

  # Score vector in order of ranking (leftmost is the top result)
  scores = []
  
  for result in searcher.search(bqm.main_query, bqm.sentiment_query, limit=limit):
    score_app = bqm.get_score(result['comment_id'])
    if score_app is not None:
      scores.append(score_app)
    else:
      print("\n" * 10)
      
      print(f"Sentiment: {result['sentiment'].human_readable(0.1)}")
      print(f"Show: {result['title']} - Episode {result['episode']}")
      print("-"*20)
      print(result['content'])
      print("-"*20)
      score_app=common_utils.controllo_interi.verifica()
      print("\n"*10)
      bqm.update_score(result['comment_id'], score_app)     
      scores.append(score_app)

    #non scrivere mentre guidi non rischiare!! 
  return scores

def run(index_dir, benchmark_dir):
  index_dir = pathlib.Path(index_dir)
  benchmark_dir = pathlib.Path(benchmark_dir)

  index = whoosh.index.open_dir(str(index_dir), readonly=True)
  searcher = app.SearchEngine()
  searcher.set_index(index)

  dcg_by_query = []
  idcg_lb_by_query = []
  results = []

  for query_file in benchmark_dir.glob('*.json'):
    with benchmarking.BenchmarkQueryManager(query_file) as bqm:
      # The relevance score of each result
      scores = run_single_query(searcher, bqm)

      # Lower bound for the Ideal DCG for this query
      # (it's very likely that we didn't rate all relevant documents!)
      query_idcg_lb = benchmarking.dcg.compute_ideal_DCG(bqm.iter_scores())
    
    # Discounted Cumulative Gain for this query
    query_dcg = benchmarking.dcg.compute_DCG(scores)

    dcg_by_query.append(query_dcg)
    idcg_lb_by_query.append(query_idcg_lb)
    results.append(benchmarking.results.QueryResults(query_dcg, query_idcg_lb, bqm.main_query, bqm.sentiment_query))

  # Compute the average DCG and IDCG lower bound over all the queries of this benchmark
  average_dcg = common_utils.arrays.average(*dcg_by_query)
  average_idcg_lb = common_utils.arrays.average(*idcg_lb_by_query)
  
  return benchmarking.results.BenchmarkResults(results, average_dcg, average_idcg_lb)
