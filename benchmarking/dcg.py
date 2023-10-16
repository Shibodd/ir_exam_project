from .benchmark_spec import BenchmarkQuerySpec
import numpy as np
import whoosh.index
from common_utils.arrays import largest_k


def compute_DCG(result_relevances) -> np.ndarray:
  """ Computes the Discounted Cumulative Gain for the results. """

  cumulative = np.cumsum(result_relevances)
  discounts = np.log2(np.arange(start=2, stop=len(result_relevances) + 2, dtype=int)) 
  return cumulative / discounts




def compute_ideal_DCG(index: whoosh.index.Index, dimension: int) -> np.array:
  """
  The ideal DCG is the DCG of the ideal ranking,
  in which documents are sorted by descending relevance score.
  
  dimension: Limits the ideal DCG to this size.
  """
  reader = index.reader()
  all_relevances = np.fromiter((rel for rel, _ in reader.iter_field('relevance')), dtype=int)

  if dimension > all_relevances.shape[0]:
    raise ValueError("Requested ideal DCG dimension is larger than the amount of documents in the index.")
  
  return compute_DCG(largest_k(all_relevances, dimension))


def compute_NDCG(index: whoosh.index.Index, result_relevances) -> np.ndarray:
  """
  Computes the Normalized Discounted Cumulative Gain for the results.
  """
  return compute_DCG(result_relevances) / compute_ideal_DCG(index, len(result_relevances))




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