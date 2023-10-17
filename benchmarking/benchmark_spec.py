import json
from dataclasses import dataclass
import pathlib

@dataclass
class BenchmarkQuerySpec:
  main_query: str
  sentiment_query: str
  index_dir: pathlib.Path


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
import pathlib

def parse_query_file(path):
  with open(path, 'r', encoding='utf8') as f:
    spec = json.load(f)
    
  return BenchmarkQuerySpec(
    main_query=spec['main_query'],
    sentiment_query=spec['sentiment_query'],
    index_dir=pathlib.Path(spec['index_dir'])
  )

def parse_benchmark_spec(directory):
  directory = pathlib.Path(directory)
  if not directory.is_dir():
    raise ValueError("Directory {directory} not found!")
  
  files = directory.glob("*.json")
  return [parse_query_file(path) for path in files]