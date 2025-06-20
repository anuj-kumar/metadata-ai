from pymongo import MongoClient


def get_collection(mongo_host, mongo_user, mongo_password, collection_name):
    client = MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_host}")
    db = client['ragpoc']
    return db[collection_name]
