import numpy as np

def largest_k(arr, k):
  ans = np.partition(arr, -k)[-k:]
  ans.sort()
  return np.flip(ans)