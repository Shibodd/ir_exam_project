def verifica():
  new_s = input("Enter a score (0 not relevant, 1 mildly relevant, 2 relevant): ")
  try:
    new_s=int(new_s)
    return new_s
  except:
    print("That's not a number. Try again.")
    return verifica()