import os 

from dotenv import load_dotenv
from pymongo import AsyncMongoClient


load_dotenv()


mongodb_uri = os.getenv("MONGODB_URI")
mongodb_db = os.getenv("MONGODB_DB", "coinwise")


if not mongodb_uri:
    raise ValueError("Mongo db uri is missing from env.")

client = AsyncMongoClient(mongodb_uri)
database = client[mongodb_db]

users_collection = database["users"]
documents_collection = database["documents"]
chats_collection = database["chats"]
