from pymongo import MongoClient
from dotenv import load_dotenv

"""Includes code required to connect to the db
"""

def get_database():
    """Returns the correct collection from mongodb database

    Returns:
        Collection that holds the piece rules for the game
    """
    load_dotenv()
    connection_string = "mongodb+srv://ToukoPuro:valiaikainenkurssiavarten@cluster0.9ftzk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    return client['piece_rules']


def insert_piece_to_db(json):
    dbname = get_database()
    collection_name = dbname["piece_rules"]
    collection_name.insert_one(json)


def get_db_pieces():
    """Returns the piece rules from mongodb database

    Returns:
        JSON that represents the saved piece rules that RuleReader knows how to parse
    """
    dbname = get_database()
    collection_name = dbname["piece_rules"]
    return collection_name.find()

def upload_piece(params):
    """Uploads piece rules to mongodb. 

    Args:
        params {name: str, rules: list[Rule]}: Is dictionary since it's used in input_phase.
        Has the name and rules of the piece to upload
    """

    json = {
        "name": params["name"]
    }
    json["rules"] = [rule.to_json() for rule in params["rules"]]
    insert_piece_to_db(json)
