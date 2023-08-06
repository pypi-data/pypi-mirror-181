def _isfloat(num):
  try:
    float(num)
    return True
  except (ValueError, TypeError):
    return False
