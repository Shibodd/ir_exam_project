import benchmarking.interactive
import benchmarking.visualization
import numpy as np
import argparse
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('index_dir')
  parser.add_argument('benchmark_dir')
  parser.add_argument('-g', '--graphic', action='store_true', help='Visualizes plots as well as text.')
  parser.add_argument('-i', '--interactive', action='store_true', help='Benchmark edit mode.')
  args = parser.parse_args()

  np.set_printoptions(precision=2)

  try:
    results = benchmarking.interactive.run(args.index_dir, args.benchmark_dir, args.interactive)

    benchmarking.visualization.visualize_results_text(results)
    if args.graphic:
      benchmarking.visualization.visualize_results_plots(results)

  except KeyboardInterrupt:
    pass

  return 0

if __name__ == '__main__':
  exit(main())