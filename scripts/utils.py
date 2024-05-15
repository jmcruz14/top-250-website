import re
from datetime import datetime, timedelta

def extract_numeric_text(tag) -> int:
  try:
    return int(re.sub(r"[^0-9]", '', tag))
  except Exception:
    return None

def convert_to_asia_tz(datetime_str: str) -> datetime:
  # Convert string to datetime object
  timestamp_dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

  # Define GMT +8 timezone offset
  gmt_offset = timedelta(hours=8)

  # Check if the timestamp is within 8 hours of GMT +8
  # BUG: fix timestamp equation as it does not dynamically account for timezones not UTC +0
  if timestamp_dt.utcoffset() is not None and timestamp_dt.utcoffset() != gmt_offset:
      timestamp_dt = timestamp_dt - (timestamp_dt.utcoffset() - gmt_offset)
  else:
      timestamp_dt = timestamp_dt + gmt_offset
  return timestamp_dt