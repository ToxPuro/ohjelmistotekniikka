from pymongo import MongoClient
import pymongo
import os
from dotenv import load_dotenv

def get_database():
    load_dotenv()
    PASSWORD = os.environ.get("PASSWORD")
    CONNECTION_STRING = f"mongodb+srv://ToukoPuro:{PASSWORD}@cluster0.9ftzk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client['piece_rules']

def insert_piece_to_db(json):
    dbname = get_database()
    collection_name = dbname["piece_rules"]
    collection_name.insert_one(json)

def get_db_pieces():
    dbname = get_database()
    collection_name = dbname["piece_rules"]
    return collection_name.find()


