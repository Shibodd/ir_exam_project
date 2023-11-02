if __name__ != '__main__':
  exit()
  
import whoosh.index
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('index_directory')
args = parser.parse_args()

print(whoosh.index.open_dir(args.index_directory).doc_count())