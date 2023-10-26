from dataclasses import dataclass
import numpy as np

@dataclass
class BenchmarkResults:
  dcg_by_query: list[np.ndarray]
  idcg_lb_by_query: list[np.ndarray]
  average_dcg: np.ndarray
  average_idcg_lb: np.ndarray