def query_to_string(main_query: str, sentiment_query: str):
  return f"content:({main_query}) AND sentiment:({sentiment_query})"