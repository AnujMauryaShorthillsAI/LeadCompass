from pymongo import MongoClient
import os
import time
from dotenv import load_dotenv
import pandas as pd
from pymongo import UpdateOne
from pymongo import InsertOne

load_dotenv()

DB_NAME = "lead_compass"

SOURCE_MORTGAGE = "sam_filter"

TARGET_INDIVIDUAL = "individual_borrowers"
TARGET_COMPANY = "company_borrowers"

# MONGO_CONNECTION_URL = os.getenv("mongodb://localhost:27017")

client = MongoClient("mongodb://localhost:27017")

# Access a specific database (replace 'your_database' with your actual database name)
db = client[DB_NAME]
collection_project = db["project"]

def get_current_time():
    return time.time()


st = get_current_time()

collection_source_mortgage = db[SOURCE_MORTGAGE]

collection_individual = db[TARGET_INDIVIDUAL]
collection_company = db[TARGET_COMPANY]

st = get_current_time()

latest_project = collection_project.find_one({}, sort=[("_id", -1)])
latest_project_id = latest_project.get("project_id", 0)

filter_mortgage = {
    "$and": [
        {"residential_tag": 1},
        {"time_tag": "N"},
        {"project_id": latest_project_id}
    ]
}

# Dealing with sam collection
batch_size = 1000

count = 0

cursor = collection_source_mortgage.find(filter_mortgage)

to_insert_company = []
to_insert_individual = []

for document in cursor:
    count += 1
    if "_id" in document:
        del document["_id"]

    if count % batch_size == 0:
        print(count)
        result1 = collection_company.bulk_write(to_insert_company)
        result2 = collection_individual.bulk_write(to_insert_individual)

        to_insert_company = []
        to_insert_individual = []

    if document["company_tag_cal_b1"] != "" or document["company_tag_given_b1"] != "":
        document["Source"] = "SAM"
        document["Borrower"] = document["borrower1_full_name"]
        if document["borrower2_full_name"] == "":
            document["PartialLoanAmount"] = document["LoanAmount"]
        else:
            document["PartialLoanAmount"] = document["LoanAmount"] // 2
        to_insert_company.append(InsertOne(document.copy()))

    if document["company_tag_cal_b2"] != "" or document["company_tag_given_b2"] != "":
        document["Source"] = "SAM"
        document["Borrower"] = document["borrower2_full_name"]
        if document["borrower1_full_name"] == "":
            document["PartialLoanAmount"] = document["LoanAmount"]
        else:
            document["PartialLoanAmount"] = document["LoanAmount"] // 2
        to_insert_company.append(InsertOne(document.copy()))

    if document["borrower1_full_name"] != "" and (int(document["OriginalDateOfContract"]) > 20230000) and \
            document["company_tag_cal_b1"] == "" and document["company_tag_given_b1"] == "":
        document["Source"] = "SAM"

        document["Borrower"] = document["borrower1_full_name"]
        if document["borrower2_full_name"] == "":
            document["PartialLoanAmount"] = document["LoanAmount"]
        else:
            document["PartialLoanAmount"] = document["LoanAmount"] // 2
        to_insert_individual.append(InsertOne(document.copy()))

    if document["borrower2_full_name"] != "" and (int(document["OriginalDateOfContract"]) > 20230000) and \
            document["company_tag_cal_b2"] == "" and document["company_tag_given_b2"] == "":
        document["Source"] = "SAM"
        document["Borrower"] = document["borrower2_full_name"]
        if document["borrower1_full_name"] == "":
            document["PartialLoanAmount"] = document["LoanAmount"]
        else:
            document["PartialLoanAmount"] = document["LoanAmount"] // 2
        to_insert_individual.append(InsertOne(document.copy()))

result1 = collection_company.bulk_write(to_insert_company)
result2 = collection_individual.bulk_write(to_insert_individual)

et = get_current_time()

print(f"Done with flattening mortgage collection {et - st} seconds")

client.close()
