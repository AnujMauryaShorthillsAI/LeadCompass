from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_username = os.getenv("db_username")
db_password = os.getenv("db_password")
db_name = os.getenv("db_name")

MONGO_URL = "mongodb+srv://user:admin@leadcompass.auduirj.mongodb.net/?retryWrites=true&w=majority"

class Database:
    def __init__(self) -> None:
        self.client = None

    def get_db_connection(self):
        if not self.client:
            try:
                self.client = MongoClient(MONGO_URL)
                print("Connected to MongoDB successfully")
            except ConnectionError as ex:
                print("Error connecting to MongoDB:", ex)

        return self.client

    def get_collection(self, collection_name):
        if not self.client:
            self.get_db_connection()
            if not self.client:
                raise Exception("No database connection.")
        return self.client[db_name][collection_name]


database = Database()

def get_collection(collection_name):
    collection = database.get_collection(collection_name)
    return collection

