### About

Recorded list of errors obtained in the process of developing this application.
Might be useful documentation for people looking to implement this app in their local
build.

- `ServerSelectionTimeoutError ... [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1006)`

**Error found in the following code**:
```Python
client = MongoClient(uri)
```

**Solution**:
```Python
client = MongoClient(uri, tlsCAFile=certifi.where())
```

When connecting to the DB, pymongo defaultly relies on the OS's root certificates. Certification verification
fails because OpenSSL does not have access to the root certificates / the certificates are out of date.

Source: [Link](https://www.mongodb.com/community/forums/t/serverselectiontimeouterror-ssl-certificate-verify-failed-trying-to-understand-the-origin-of-the-problem/115288)

- `Enable tracemalloc to get traceback where the object was allocated`

So in general when running tests on FastAPI, the app tends to return a warning stating that we should implement `tracemalloc` to track
memory usage. 

**Solution**:
Implement the following code as middleware in the FastAPI application.

```Python
@app.middleware('http')
async def log_memory_usage(request: Request, call_next):
  start_time = time.time()
  snapshot1 = tracemalloc.take_snapshot()
  response = await call_next(request)
  snapshot2 = tracemalloc.take_snapshot()
  
  stats = snapshot2.compare_to(snapshot1, 'lineno')
  top_stats = stats[:10]

  print(f"Memory usage for {request.url.path}")
  for stat in top_stats:
      print(stat)
  
  process_time = time.time() - start_time
  print(f"Request processing time: {process_time:.4f} sec")
  
  return response
```

- `unhashable type: dict / pydantic class`

A Pydantic BaseClass is not hashable.