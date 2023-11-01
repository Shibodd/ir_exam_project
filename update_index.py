import sentiment.schema
import argparse
from dataclasses import dataclass
from whoosh import index, fields
import shutil
import pathlib

@dataclass
class Version:
  name: str
  schema: fields.Schema
  update_fn: callable


VERSIONS = [
  Version('v1', sentiment.schema.SCHEMA_V1, None),
  Version('v2', sentiment.schema.SCHEMA_V2, sentiment.schema.schema_update_just_copy),
  Version('v3', sentiment.schema.SCHEMA_V3, sentiment.schema.schema_update_just_copy),
]

class UnknownVersionException(Exception):
  pass

class DifferentSchemaException(Exception):
  pass

class BadVersionPairException(Exception):
  pass


def update(from_version, to_version, indexdir):
  def get_version_index(name):
    return next(i for i in range(len(VERSIONS)) if VERSIONS[i].name == name)

  from_version_i = get_version_index(from_version)
  if from_version_i is None:
    raise UnknownVersionException("From version is unknown.")
  
  to_version_i = get_version_index(to_version)
  if to_version_i is None:
    raise UnknownVersionException("To version is unknown.")
  
  if from_version_i > to_version_i:
    raise BadVersionPairException("Downgrading to a previous version is not supported.")

  if from_version_i == to_version_i:
    raise BadVersionPairException("You specified the same from and to versions.")

  indexdir = pathlib.Path(indexdir)

  # Check index has correct schema
  idx = index.open_dir(indexdir)
  if idx.schema != VERSIONS[from_version_i].schema:
    raise DifferentSchemaException()
  del idx
  
  current_directory = pathlib.Path(indexdir)
  old_directory = None
  for i in range(from_version_i + 1, to_version_i + 1):
    version = VERSIONS[i]

    next_directory = pathlib.Path(f"{str(indexdir)}_{version.name}")

    current_idx = index.open_dir(str(current_directory))

    if not next_directory.exists():
      next_directory.mkdir()
      
    next_idx = index.create_in(next_directory, version.schema)

    with current_idx.reader() as reader, next_idx.writer() as writer:
      version.update_fn(reader, writer)

    if old_directory and old_directory != indexdir:
      shutil.rmtree(old_directory)

    old_directory = current_directory
    current_directory = next_directory

  if old_directory and old_directory != indexdir:
      shutil.rmtree(old_directory)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('indexdir')
  parser.add_argument('from_version')
  parser.add_argument('to_version')

  args = parser.parse_args()
  update(args.from_version, args.to_version, args.indexdir)