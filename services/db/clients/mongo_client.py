from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
mongo = MongoClient(MONGO_URL)
db = mongo["aihome"]
