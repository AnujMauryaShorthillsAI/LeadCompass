from pymongo import MongoClient
import os
import time
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "lead_compass"
SOURCE = "company_borrowers"

# MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")

client = MongoClient("mongodb://localhost:27017")

# Access a specific database (replace 'your_database' with your actual database name)
db = client[DB_NAME]


def get_current_time():
    return time.time()


et = get_current_time()

print("Started tagging company_borrowers")

st = get_current_time()
collection_source = db[SOURCE]
collection_source.create_index([("Borrower", 1)])


pipeline = [
    {
        "$match": {
            "Borrower": {"$regex": r"\btrust\b", "$options": "i"}
        }
    },
    {
        "$group": {
            "_id": "$Borrower",
            "TotalPartialLoanAmount": {"$sum": "$PartialLoanAmount"},
        }
    },
    {
        "$match": {
            "TotalPartialLoanAmount": {"$lt": 1000000}
        }
    },
    {
        "$project": {
            "_id": 0,
            "Borrower": "$_id",
            "TotalPartialLoanAmount": 1
        }
    }
]

result = list(collection_source.aggregate(pipeline))

borrower_list_with_name_trust_net_loan_amount_less_than_million = [entry["Borrower"] for entry in result]

# Update each row in the collection
for borrower in borrower_list_with_name_trust_net_loan_amount_less_than_million:
    collection_source.update_many(
        {"Borrower": borrower},
        {"$set": {"RcCalIsTrust&NetLoanLessThanMillion": "Y"}}
    )

# Update rows where Borrower is not in the list
collection_source.update_many(
    {"Borrower": {"$nin": borrower_list_with_name_trust_net_loan_amount_less_than_million}},
    {"$set": {"RcCalIsTrust&NetLoanLessThanMillion": "N"}}
)

et = get_current_time()

print(f"Time taken in tagging company borrowers is {et - st} seconds")
