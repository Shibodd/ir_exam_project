import numpy as np

def largest_k(arr: np.ndarray, k: int) -> np.ndarray:
  ans = np.partition(arr, -k)[-k:]
  ans.sort()
  return np.flip(ans)

def average(*arrays: np.ndarray, sentinel=-1000) -> np.ndarray:
  maxlen = max(r.shape[0] for r in arrays)
  padded_arrays = tuple(np.pad(r, (0, maxlen - r.shape[0]), constant_values=sentinel) for r in arrays)
  stacked = np.vstack(padded_arrays)
  return np.average(stacked, axis=0, weights=(stacked != sentinel))