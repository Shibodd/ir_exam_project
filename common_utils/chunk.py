import itertools

def chunk(iterable, chunk_size):
  while True:
    chunk = list(itertools.islice(iterable, 0, chunk_size))
    if chunk:
      yield chunk
    else:
      break