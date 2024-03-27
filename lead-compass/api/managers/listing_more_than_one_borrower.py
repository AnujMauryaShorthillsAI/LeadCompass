from pymongo import MongoClient
import os
import time
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "lead_compass"
SOURCE = "individual_borrowers"

# MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")

client = MongoClient("mongodb://localhost:27017")

# Access a specific database (replace 'your_database' with your actual database name)
db = client[DB_NAME]


def get_current_time():
    return time.time()


st = get_current_time()

collection_source = db[SOURCE]
collection_source.create_index([("Borrower", 1)])

pipeline = [
    {
        "$group": {
            "_id": "$Borrower",
            "count": {"$sum": 1}
        }
    },
    {
        "$match": {
            "count": {"$gt": 1}
        }
    },
    {
        "$project": {
            "_id": 0,
            "Borrower": "$_id",
            "count": 1
        }
    }
]

result = list(collection_source.aggregate(pipeline))

# Extract Borrowers with count greater than one to a list
borrowers_list = [entry["Borrower"] for entry in result]
print(len(borrowers_list))

# Update each row in the collection
for borrower in borrowers_list:
    collection_source.update_many(
        {"Borrower": borrower},
        {"$set": {"morethanone": "Y"}}
    )

# Update rows where Borrower is not in the list
collection_source.update_many(
    {"Borrower": {"$nin": borrowers_list}},
    {"$set": {"morethanone": "N"}}
)

print("Update completed.")
