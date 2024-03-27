from pymongo import MongoClient
import os, sys, time
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "lead_compass"
SOURCE_I = "individual_borrowers"
SOURCE_C = "company_borrowers"
TARGET = "mvp"

MONGO_CONNECTION_URL = os.getenv("mongodb://localhost:27017")

client = MongoClient(MONGO_CONNECTION_URL)

# Access a specific database (replace 'your_database' with your actual database name)
db = client[DB_NAME]


def get_current_time():
    return time.time()


st = get_current_time()

collection_individual = db[SOURCE_I]
collection_company = db[SOURCE_C]
collection_project = db["project"]

# New collection
new_collection = db[TARGET]
latest_project = collection_project.find_one({}, sort=[("_id", -1)])
latest_project_id = latest_project.get("project_id", 0)
# Define your filter criteria
filter_criteria_i = {"project_id": latest_project_id}
# filter_criteria_i = {}
filter_criteria_c = {"$and": [
    {"RcCalIsTrust&NetLoanLessThanMillion": "N"},
    {"project_id": latest_project_id}
]
}

# Define the fields you want to select and rename
fields_to_select_i = {
    "RcCalBorrower": "$Borrower",
    "LoanAmount": "$LoanAmount",

    "RcCalPartialLoanAmount": "$PartialLoanAmount",
    "TransactionId": "$PID",

    "PropertyFullStreetAddress": "$PropertyFullStreetAddress",
    "PropertyZipCode": "$PropertyZipCode",
    "PropertyZip4": "$PropertyZip4",
    "PropertyUnitType": "$PropertyUnitType",
    "PropertyUnitNumber": "$PropertyUnitNumber",
    "PropertyState": "$PropertyState",
    "PropertyCityName": "$PropertyCityName",

    "BuyerMailFullStreetAddress": "$BuyerMailFullStreetAddress",
    "BuyerMailZipCode": "$BorrowerMailZipCode",
    "BuyerMailZip4": "$BorrowerMailZip4",
    "BuyerMailUnitType": "$BorrowerMailUnitType",
    "BuyerMailUnitNumber": "$BorrowerMailUnitNumber",
    "BuyerMailState": "$BorrowerMailState",
    "BuyerMailCity": "$BorrowerMailCity",

    "OriginalDateOfContract": "$OriginalDateOfContract",
    "LenderNameBeneficiary": "$LenderNameBeneficiary",

    "FIPSCode": '$FIPSCode',
    "APN": '$APN',
    "DPID": '$DPID',
    "_id": 0,
    "RcCalSource": "$Source",
    "ProjectId": "$project_id",
    "RcCalType": "I"
}

fields_to_select_c = {
    "RcCalBorrower": "$Borrower",
    "LoanAmount": "$LoanAmount",

    "RcCalPartialLoanAmount": "$PartialLoanAmount",
    "TransactionId": "$PID",

    "PropertyFullStreetAddress": "$PropertyFullStreetAddress",
    "PropertyZipCode": "$PropertyZipCode",
    "PropertyZip4": "$PropertyZip4",
    "PropertyUnitType": "$PropertyUnitType",
    "PropertyUnitNumber": "$PropertyUnitNumber",
    "PropertyState": "$PropertyState",
    "PropertyCityName": "$PropertyCityName",

    "BuyerMailFullStreetAddress": "$BuyerMailFullStreetAddress",
    "BuyerMailZipCode": "$BorrowerMailZipCode",
    "BuyerMailZip4": "$BorrowerMailZip4",
    "BuyerMailUnitType": "$BorrowerMailUnitType",
    "BuyerMailUnitNumber": "$BorrowerMailUnitNumber",
    "BuyerMailState": "$BorrowerMailState",
    "BuyerMailCity": "$BorrowerMailCity",

    "OriginalDateOfContract": "$OriginalDateOfContract",
    "LenderNameBeneficiary": "$LenderNameBeneficiary",

    "FIPSCode": '$FIPSCode',
    "APN": '$APN',
    "DPID": '$DPID',
    "_id": 0,
    "RcCalSource": "$Source",
    "ProjectId": "$project_id",
    "RcCalType": "C"
}

# Aggregation pipeline to filter and rename fields
pipeline_i = [
    {"$match": filter_criteria_i},
    {"$project": fields_to_select_i}
]

pipeline_c = [
    {"$match": filter_criteria_c},
    {"$project": fields_to_select_c}
]

# Aggregate and insert the filtered documents into the new collection
# print(collection_individual.aggregate(pipeline_i))
new_collection.insert_many(collection_individual.aggregate(pipeline_i))
new_collection.insert_many(collection_company.aggregate(pipeline_c))

# Close MongoDB connection
client.close()
