'''This Python script serves as the conversion layer of API calls from the Nuxt/JS
layer of the app to the FastAPI portion of the app.'''

# def match_array(key: str, vals: list[str]) -> dict:
  
def agg_ops_dict(measure: str, key: str | list, vals: list | None = None) -> dict | bool:
  # v1.0 support: $avg, $add, $count
  try:
    if measure == 'mean':
      return { 
        "$group": {
          "_id": None,
          'avgQty': { "$avg": "$" + key }
        }
      }
    if measure == 'sum':
      return { '$group': {
        "_id": None,
        'totalSum': { "$sum": key }}
      } 
    
    else:
      raise Exception
  except Exception as e:
    print(f"error noticed {e}")