from dataclasses import dataclass
import numpy as np

@dataclass
class QueryResults:
  dcg: np.ndarray
  idcg_lb: np.ndarray
  main_query: str
  sentiment_query: str

@dataclass
class BenchmarkResults:
  results_by_query: list[QueryResults]
  average_dcg: np.ndarray
  average_idcg_lb: np.ndarray
