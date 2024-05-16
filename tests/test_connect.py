import os
import pprint
import certifi
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import urllib.parse as parse
import motor

from pymongo.mongo_client import MongoClient
load_dotenv()

MONGODB_UNAME = parse.quote_plus(os.environ['MONGODB_USERNAME'])
# MONGODB_UNAME = parse.quote_plus('jcmcruz14')
MONGODB_PW = parse.quote_plus(os.environ['MONGODB_PASSWORD'])
# MONGODB_PW = parse.quote_plus('tutorial')

# change uri if tutorial db is tested

def test_connection(username: str, password: str):
  uri = f"mongodb+srv://{MONGODB_UNAME}:{MONGODB_PW}@top-250-filipino-v1.01jik2w.mongodb.net/?retryWrites=true&w=majority&appName=top-250-filipino-v1"
  # Create a new client and connect to the server
  client = MongoClient(uri, tlsCAFile=certifi.where())
  # Send a ping to confirm a successful connection
  try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
      pprint.pp(e)

async def test_query_data(uri):
   client = AsyncIOMotorClient(uri, tlsCAFile=certifi.where())
   db = client.get_database("sample_mflix")
   test_collection = db.get_collection("movies")
   # Query the collection to retrieve documents
   documents = await test_collection.find().to_list(10)
   json_equivalent = [doc for doc in documents]
   print(type(db))
   print(type(documents))
   print('=========')
   print(json_equivalent)

if __name__ == '__main__':
   uri = f"mongodb+srv://{MONGODB_UNAME}:{MONGODB_PW}@top-250-filipino-v1.01jik2w.mongodb.net/?retryWrites=true&w=majority&appName=top-250-filipino-v1"
   test_connection(MONGODB_UNAME, MONGODB_PW)
   asyncio.run(test_query_data(uri))