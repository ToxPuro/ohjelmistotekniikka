from pymongo import MongoClient
from dotenv import load_dotenv


def get_database():
    load_dotenv()
    connection_string = "mongodb+srv://ToukoPuro:valiaikainenkurssiavarten@cluster0.9ftzk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    return client['piece_rules']


def insert_piece_to_db(json):
    dbname = get_database()
    collection_name = dbname["piece_rules"]
    collection_name.insert_one(json)


def get_db_pieces():
    dbname = get_database()
    collection_name = dbname["piece_rules"]
    return collection_name.find()

def upload_piece(name, rules):
    json = {
        "name": name
    }
    json["rules"] = [rule.to_json() for rule in rules]
    insert_piece_to_db(json)
