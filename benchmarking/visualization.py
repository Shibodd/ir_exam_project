from .results import BenchmarkResults

def visualize_results_text(results: BenchmarkResults):
  """ TODO: Visualizzazione decente testuale """
  print(results.dcg_by_query)
  print(results.idcg_lb_by_query)
  print(results.average_dcg)
  print(results.average_idcg_lb)

def visualize_results_plots(results: BenchmarkResults):
  """ TODO: Visualizzazione figa con grafici """
  raise NotImplementedError("Te piacesse")