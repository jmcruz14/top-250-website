import os
import pprint
import json
import certifi
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import urllib.parse as parse

from pymongo.mongo_client import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
load_dotenv()

MONGODB_UNAME = parse.quote_plus(os.environ['MONGODB_USERNAME'])
MONGODB_PW = parse.quote_plus(os.environ['MONGODB_PASSWORD'])
MONGODB_HOST = os.environ['MONGODB_HOST']
LBOXD_COLLECTION = os.environ['LBOXD_COLLECTION']

async def connect_server() -> AsyncIOMotorClient | None:
  uri = f"mongodb+srv://{MONGODB_UNAME}:{MONGODB_PW}@{MONGODB_HOST}"
  try:
    client = AsyncIOMotorClient(
      uri, 
      tlsCAFile=certifi.where(),
      uuidRepresentation='standard'
    )
    print("Pinged your deployment. You successfully connected to MongoDB!")
    return client
  except ServerSelectionTimeoutError as serverError:
    print('Server error detected:', serverError)
  except Exception as e:
    print('Error detected:', e)
  return None

async def query_db(client, query, collection, limit: int = 1) -> list:
  # client = await connect_server() # RuntimeWarning: coroutine was never awaited -- attach await to async func
  # NOTE: solve error for runtime warning: enable tracemalloc to get object allocation traceback
  db = client.get_database(LBOXD_COLLECTION)
  collection = db.get_collection(collection)
  documents = await collection.find(query).to_list(limit)
  obj = [doc for doc in documents]
  # client.close()
  return obj

async def update_db(client, document, collection):
  db = client.get_database(LBOXD_COLLECTION)
  collection = db.get_collection(collection)
  collection.insert_one(document)
  print('Document has been added!')

async def delete_docs(client, query: dict, collection, single: bool):
  db = client.get_database(LBOXD_COLLECTION)
  collection_name = collection
  collection = db.get_collection(collection)
  if single:
    count_ = 1
    await collection.delete_one(query)
  else:
    res = await collection.delete_many(query)
    count_ = res.deleted_count
  print(f'{count_} documents have been deleted from {collection_name}!')

if __name__ == '__main__':
   asyncio.run(connect_server())