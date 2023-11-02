from .results import BenchmarkResults
import benchmarking.creation_graph as creation_graph
import app.query_to_string

def visualize_results_text(results: BenchmarkResults):
  for query in results.results_by_query:
    print("\n")
    print(app.query_to_string.query_to_string(query.main_query, query.sentiment_query))
    print("DCG:")
    print(query.dcg)
    print("Lower bound for IDCG:")
    print(query.idcg_lb)

  print("\nAverage:")
  print(results.average_dcg)
  print(results.average_idcg_lb)
  

def visualize_results_plots(results: BenchmarkResults):
  for result in results.results_by_query:
    text_query=app.query_to_string.query_to_string(result.main_query,result.sentiment_query)
    creation_graph.creazione_grafico(result.dcg,result.idcg_lb,text_query)
    
  creation_graph.creazione_grafico(results.average_dcg, results.average_idcg_lb, "Average results")