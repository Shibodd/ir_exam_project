from sentiment.schema import SCHEMA as BASE_SCHEMA
import whoosh.fields

SCHEMA = BASE_SCHEMA.copy()
SCHEMA.add("relevance", whoosh.fields.NUMERIC(stored=True))