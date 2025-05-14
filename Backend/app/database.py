from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["file_sharing"]

def init_db():
    print("DB Initialized")
