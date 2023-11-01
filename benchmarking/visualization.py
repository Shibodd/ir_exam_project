from .results import BenchmarkResults
import matplotlib.pyplot as plt
import benchmarking.creation_graph as creation_graph

def visualize_results_text(results: BenchmarkResults):
  """ TODO: Visualizzazione decente testuale """
  
  print(results.results_by_query)
  print(results.average_dcg)
  print(results.average_idcg_lb)
  

def visualize_results_plots(results: BenchmarkResults):
  """ TODO: Visualizzazione figa con grafici """
  for result in results.results_by_query:
    creation_graph.creazione_grafico(result.dcg,result.idcg_lb)
  print()
  creation_graph.creazione_grafico(results.average_dcg,results.average_idcg_lb)

raise NotImplementedError("Te piacesse")