def input_integer(msg, min, max):
  while True:
    try:
      relevance = int(input(msg))
      if relevance >= min and relevance <= max:
        return relevance
      print(f"Must be an integer between {min} and {max}.")
    except ValueError:
      print("Must be an integer.")