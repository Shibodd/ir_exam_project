import benchmarking.interactive
import benchmarking.visualization

import argparse
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('index_dir')
  parser.add_argument('benchmark_dir')
  parser.add_argument('-g', '--graphic', action='store_true', help='Visualizes plots as well as text.')
  args = parser.parse_args()

  try:
    results = benchmarking.interactive.run(args.index_dir, args.benchmark_dir)

    benchmarking.visualization.visualize_results_text(results)
    if args.graphic:
      benchmarking.visualization.visualize_results_plots(results)

  except KeyboardInterrupt:
    pass

  return 0

if __name__ == '__main__':
  exit(main())