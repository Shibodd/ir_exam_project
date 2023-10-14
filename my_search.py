from app.searching import SearchEngine
from whoosh.index import open_dir

index = open_dir("indexdir")
searcher = SearchEngine(index)

from benchmarking import benchmark, benchmark_spec
benchmark.benchmark(searcher, benchmark_spec.read_benchmark_spec('benchmarking/benchmark.json'))

# for result in searcher.search('title:"Cyka blyat" episode:69', 'fear'):
#  print(result)