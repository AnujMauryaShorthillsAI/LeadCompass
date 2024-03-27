from pymongo import MongoClient
import os
import time
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from pymongo import UpdateOne

_ = load_dotenv(find_dotenv())
# mongo_url = os.getenv("MONGO_URL")
client = MongoClient("mongodb://localhost:27017")
db = client["lead_compass"]
collection_sam = db["complete_sam"]
collection_sam_filter = db["sam_filter"]
collection_project = db["project"]


def get_current_time():
    return time.time()


st = get_current_time()
latest_project = collection_project.find_one({}, sort=[("_id", -1)])
latest_project_id = latest_project.get("project_id", 0)

filter = {
    "$and": [
        # {
        #     "$or": [
        #         {"company_tag_cal_b1": {"$ne": ""}},
        #         {"company_tag_given_b1": {"$ne": ""}},
        #     ]
        # },
        {
            "$or": [
                {"ResidentialIndicator": 1},
                {"PropertyUseCode": {
                    "$in": ["APT", "COM", "COP", "EXE", "CND", "IMP", "LAN", "MFD", "MIX", "NEW", "PUD", "SFR", "RES",
                            "TWN"]}},
            ]
        },
        {"time_tag": "N"},
        {"project_id": latest_project_id}
    ]
}

# Dealing with deed collection
total_documents = collection_sam.count_documents(filter)

print("Documents filtered")

print(total_documents)

batch_size = 1000

skip = 0
while skip < total_documents:
    print(skip)
    # Fetch documents in batches
    cursor = collection_sam.find(filter).skip(skip).limit(batch_size)

    # Create a list to store the documents in the batch
    batch_documents = list(cursor)

    for document in batch_documents:
        del document['_id']

    # Insert the batch of documents into the target collection
    collection_sam_filter.insert_many(batch_documents)

    # Update the skip value for the next batch
    skip += batch_size

et = get_current_time()

print(f"total time taken in filtering mortgage {et-st} seconds")

client.close()
