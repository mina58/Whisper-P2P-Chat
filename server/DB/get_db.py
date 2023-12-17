from pymongo import MongoClient


def get_db():
    mongo_uri = "mongodb://localhost:27017/"
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client.whisper_server
    return db
