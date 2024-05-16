import re
from datetime import datetime, timezone

def extract_numeric_text(tag) -> int:
  try:
    return int(re.sub(r"[^0-9]", '', tag))
  except Exception:
    return None

def convert_to_dt(datetime_str: str) -> datetime:
  # Convert string to datetime object
  timestamp_dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

  return timestamp_dt

def strip_tz(datetime_dt: datetime) -> datetime:
  dt = datetime.fromisoformat(str(datetime_dt))

  # Remove the timezone information
  dt_without_tz = dt.replace(tzinfo=None)

  # Format back to string without the timezone
  cleaned_datetime_str = dt_without_tz.isoformat()
  
  # Return as datetime
  return cleaned_datetime_str

