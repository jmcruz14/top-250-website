import os
import pprint
import json
import certifi
import asyncio
from logging import info
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import urllib.parse as parse

from pymongo.errors import ServerSelectionTimeoutError
load_dotenv()

MONGODB_UNAME = parse.quote_plus(os.environ['MONGODB_USERNAME'])
MONGODB_PW = parse.quote_plus(os.environ['MONGODB_PASSWORD'])
MONGODB_HOST = os.environ['MONGODB_HOST']
LBOXD_COLLECTION = os.environ['LBOXD_COLLECTION']

async def connect_server(app: FastAPI) -> AsyncIOMotorClient | None:
  uri = f"mongodb+srv://{MONGODB_UNAME}:{MONGODB_PW}@{MONGODB_HOST}"
  try:
    app.mongodb_client = AsyncIOMotorClient(
      uri, 
      tlsCAFile=certifi.where(),
      uuidRepresentation='standard'
    )
    app.database = app.mongodb_client.get_default_database(LBOXD_COLLECTION)
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    
    yield
    app.mongodb_client.close()
  #   print("Pinged your deployment. You successfully connected to MongoDB!")
  #   return client
  except ServerSelectionTimeoutError as serverError:
    print('Server error detected:', serverError)
  except Exception as e:
    print('Error detected:', e)
  # return None

async def query_db(client: AsyncIOMotorClient, query: dict, collection: str, limit: int = 1) -> list:
  # client = await connect_server() # RuntimeWarning: coroutine was never awaited -- attach await to async func
  # NOTE: solve error for runtime warning: enable tracemalloc to get object allocation traceback

  collection = client.get_collection(collection)
  documents = await collection.find(query).to_list(limit)
  obj = [doc for doc in documents]
  return obj

async def update_db(client: AsyncIOMotorClient, document: dict, collection: str):
  collection = client.get_collection(collection)
  collection.insert_one(document)
  print('Document has been added!')

async def delete_docs(client: AsyncIOMotorClient, query: dict, collection: str, single: bool):
  collection = client.get_collection(collection)
  if single:
    count_ = 1
    await collection.delete_one(query)
  else:
    res = await collection.delete_many(query)
    count_ = res.deleted_count
  print(f'{count_} documents have been deleted from {collection}!')

if __name__ == '__main__':
   asyncio.run(connect_server())