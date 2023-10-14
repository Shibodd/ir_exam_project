import json
from dataclasses import dataclass

@dataclass
class BenchmarkQuerySpec:
  main_query: str
  sentiment_query: str
  dataset: dict[str, int]


""" 
// Example benchmark spec
{
  "queries": [
    {
      "main_query": "Gesu' cristo",
      "sentiment_query": "disgust AND anger",
      "dataset": {
        "dm75og5": 3,
        "fak1rr9": 2
      }
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
      query['dataset']
    )
    for query in spec['queries']
  ]