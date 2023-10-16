import json
from dataclasses import dataclass

@dataclass
class BenchmarkQuerySpec:
  main_query: str
  sentiment_query: str
  index_dir: str


""" 
// Example benchmark spec
{
  "queries": [
    {
      "main_query": "Gesu' cristo",
      "sentiment_query": "disgust AND anger",
      "index_dir": "indexdir"
    }
  ]
}
"""

def read_benchmark_spec(path):
  with open(path, 'r', encoding='utf8') as f:
    spec = json.load(f)

  return [
    BenchmarkQuerySpec(
      query['main_query'],
      query['sentiment_query'],
      query['index_dir']
    )
    for query in spec['queries']
  ]