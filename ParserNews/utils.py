from pymongo import MongoClient
from pymongo.collection import Collection 

def get_database(conf) -> Collection:
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(conf.CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    dbname = client[conf.DATABASE]
    
    return dbname[conf.COLLECTION]