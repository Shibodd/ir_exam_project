from .benchmark_spec import BenchmarkQuerySpec
import numpy as np


def compute_DCG(result_relevances) -> np.ndarray:
  """ Computes the Discounted Cumulative Gain for the results. """

  cumulative = np.cumsum(result_relevances)
  discounts = np.log2(np.arange(start=2, stop=len(result_relevances) + 2, dtype=int)) 
  return cumulative / discounts


def compute_NDCG(result_relevances, query_spec: BenchmarkQuerySpec) -> np.ndarray:
  """
  Computes the Normalized Discounted Cumultaive Gain for the results.
  The ideal DCG is computed from the entire dataset (the search engine may not return all relevant documents from the dataset!).
  """

  # The ideal DCG is the DCG of the ideal ranking, which ranks the most relevant document first
  sorted_dataset_relevances = sorted((score for score in query_spec.dataset.values()), reverse=True)

  # Don't compute the ideal DCG for more ranks than there are results
  ideal_dcg = compute_DCG(sorted_dataset_relevances[:len(result_relevances)])
  
  dcg = compute_DCG(result_relevances)
  return dcg / ideal_dcg


def compute_average_NDCG(ndcg_by_query, benchmark_spec):
  """
  Computes the Average Normalize Discounted Cumulative Gain
  for the NDCGS that have been previously computed from multiple queries (with compute_NDCG)
  """

  # Decide a length for the average NDCG. Queries can have different sized datasets. Only min or max make sense.
  AVG_NDCG_LEN_FN = min # or max
  average_ndcg_length = AVG_NDCG_LEN_FN(len(query_spec.dataset) for query_spec in benchmark_spec)

  def reshape_NDCG_for_average(ndcg):
    """ Reshapes the NDCG so that it can be added to the average NDCG accumulator. """
    if AVG_NDCG_LEN_FN == min: # NDCG vector is always longer than the average NDCG
      # Just crop the array
      return ndcg[:average_ndcg_length]
    elif AVG_NDCG_LEN_FN == max: # NDCG vector is always shorter than the average NDCG
      # Pad right with the last value (Cumulative)
      return np.pad(ndcg, pad_width=(0, len(ndcg) - average_ndcg_length), mode='edge')
    
  return sum(reshape_NDCG_for_average(ndcg) for ndcg in ndcg_by_query) / len(ndcg_by_query)