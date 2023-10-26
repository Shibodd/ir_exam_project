import numpy as np
import whoosh.index
from common_utils.arrays import largest_k


def compute_DCG(result_relevances) -> np.ndarray:
  """ Computes the Discounted Cumulative Gain for the results. """
  cumulative = np.cumsum(result_relevances)
  discounts = np.log2(np.arange(start=2, stop=len(result_relevances) + 2, dtype=int)) 
  return cumulative / discounts



from typing import Iterable
def compute_ideal_DCG(all_scores: Iterable[int], dimension=None) -> np.array:
  """
  The ideal DCG is the DCG of the ideal ranking,
  in which documents are sorted by descending relevance score.
  
  dimension: Limits the ideal DCG to this size. If none, uses all scores.
  """
  all_relevances = np.fromiter(all_scores, dtype=int)

  if dimension is None or dimension == all_relevances.shape[0]:
    scores = np.sort(all_relevances)
  else:
    if dimension > all_relevances.shape[0]:
      raise ValueError("Requested ideal DCG dimension is larger than the amount of documents in the index.")
    scores = largest_k(all_relevances, dimension)
  
  return compute_DCG(scores)


def compute_NDCG(index: whoosh.index.Index, result_relevances) -> np.ndarray:
  """
  Computes the Normalized Discounted Cumulative Gain for the results.
  """
  return compute_DCG(result_relevances) / compute_ideal_DCG(index, len(result_relevances))