from .benchmark_spec import BenchmarkQuerySpec
import numpy as np


def compute_dcg(result_relevances) -> np.ndarray:
  cumulative = np.cumsum(result_relevances)
  discounts = np.log2(np.arange(start=2, stop=len(result_relevances) + 2, dtype=int)) 
  return cumulative / discounts


def compute_ndcg(result_relevances, query_spec: BenchmarkQuerySpec) -> np.ndarray:
  # The ideal DCG is the DCG of the ideal ranking, which ranks the most relevant document first
  sorted_dataset_relevances = sorted((score for score in query_spec.dataset.values()), reverse=True)
  ideal_dcg = compute_dcg(sorted_dataset_relevances[:len(result_relevances)])
  
  dcg = compute_dcg(result_relevances)
  return dcg / ideal_dcg