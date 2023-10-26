import benchmarking.interactive_benchmark

import argparse
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('index_dir')
  parser.add_argument('benchmark_dir')
  args = parser.parse_args()

  benchmarking.interactive_benchmark.run(args.index_dir, args.benchmark_dir)

  return 0

if __name__ == '__main__':
  exit(main())