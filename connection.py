from pymongo import MongoClient
from pymongo import ReturnDocument

class MonogoDB:
    def __init__(self, db_name):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]

    def find_one_and_update(self, collection_name, document):
            collection = self.db[collection_name]
            response = collection.find_one_and_update(
                filter={"fonte": document["fonte"], "texto": document["texto"] },  
                update={"$set": document},
                upsert=True,  
                return_document=ReturnDocument.BEFORE,  
            )
            return response