from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # test connection
    db = client["university_db"]
except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    db = None  # fallback
