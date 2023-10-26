import benchmarking.interactive
import benchmarking.visualization

import argparse
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('index_dir')
  parser.add_argument('benchmark_dir')
  args = parser.parse_args()

  results = benchmarking.interactive.run(args.index_dir, args.benchmark_dir)
  benchmarking.visualization.visualize_results_text(results)

  return 0

if __name__ == '__main__':
  exit(main())