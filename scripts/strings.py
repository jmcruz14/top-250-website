def replaceMultipleStrings(string: str) -> str:
  return string.replace('\t', '').replace('\xa0', '').replace('\n', '')