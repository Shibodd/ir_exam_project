from .results import BenchmarkResults
import matplotlib as dtb

def visualize_results_text(results: BenchmarkResults):
  """ TODO: Visualizzazione decente testuale """
  
  print(results.results_by_query)
  print(results.average_dcg)
  print(results.average_idcg_lb)
  

def visualize_results_plots(results: BenchmarkResults):
  """ TODO: Visualizzazione figa con grafici """
  dtb.plot(range(10), '--bo', label='marker for result')
  dtb.legend()
  raise NotImplementedError("Te piacesse")