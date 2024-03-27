from pymongo import MongoClient
import os
import time
from dotenv import load_dotenv
import pandas as pd
from pymongo import UpdateOne
import random
from bson.objectid import ObjectId

load_dotenv()
mongo_url = os.getenv("MONGO_URL")

client = MongoClient("mongodb://localhost:27017")
db = client["lead_compass"]
collection_sam = db["complete_sam"]
collection_project = db["project"]

def get_current_time():
    return time.time()


start_time = get_current_time()

# Define your terms and tags
terms_to_check = set(
    ["TRUST", "INC", "LLP", "LP", "LLC", "FUND", "INVESTMENTS", "CO", "PARTNERSHIP", "CORP", "PARTNERS", "LTD",
     "ASSOCIATES", "PLC", "PC", "PLLC"])

companyCodes = set(
    ["AB", "AC", "AD", "AE", "AG", "AR", "BU", "CN", "CO", "DB", "ES", "EX", "FL", "FM", "FR", "GN", "GP", "GV", "ID",
     "IL", "ME", "PA", "PR", "PT", "RL", "RT", "SL", "SP", "ST", "TR", "TS", "TT"])
field_to_check_mortgage = ["Borrower1LastNameOeCorporationName", "Borrower1FirstNameMiddleName",
                           "Borrower2FirstNameMiddleName", "Borrower2LastNameOrCorporationName"]
company_codes_fields_mortgage = ["Borrower1IDCode", "Borrower2IDCode"]
propertyUseCodeList = ["APT", "COM", "COP", "EXE", "CND", "IMP", "LAN", "MFD", "MIX", "NEW", "PUD", "SFR", "RES", "TWN"]

# Set batch size based on your system's memory constraints
batch_size = 1000

st = get_current_time()

# Get the total number of documents in the collection

last_processed_id = None

# Process data in batches
while True:
    query = {}  # You can add additional filters if needed
    print(last_processed_id)
    latest_project = collection_project.find_one({}, sort=[("_id", -1)])
    latest_project_id = latest_project.get("project_id", 0)

    query["project_id"] = latest_project_id

    if last_processed_id:
        query["_id"] = {"$gt": ObjectId(last_processed_id)}

    cursor = collection_sam.find(query).sort("_id").limit(batch_size)

    x = collection_sam.count_documents(query)

    print(x)

    if x == 0:
        print("Reached end of document")
        break  # No more documents, break out of the loop

    update_operations = []

    # Process each document in the batch
    for document in cursor:
        company_tag_cal = ""
        company_tag_given = ""
        company_tag_cal_b1 = ""
        company_tag_cal_b2 = ""
        company_tag_given_b1 = ""
        company_tag_given_b2 = ""

        residential_tag = 0

        time_tag = "N"

        for field in field_to_check_mortgage:
            if document[field]:
                for term in terms_to_check:
                    if term in document[field].upper().split(" "):
                        company_tag_cal += term
                        break
                company_tag_cal += "|"
            else:
                company_tag_cal += "|"

        company_tag_cal = company_tag_cal[:-1]

        array_1 = company_tag_cal.split("|")

        company_tag_cal_b1 = array_1[0] + array_1[1]

        company_tag_cal_b2 = array_1[2] + array_1[3]

        # if company_tag_cal == "|||":
        #     company_tag_cal = ""

        for field in company_codes_fields_mortgage:
            if (document[field]) and (document[field].strip() in companyCodes):
                company_tag_given += document[field] + "|"
            else:
                company_tag_given += "|"

        company_tag_given = company_tag_given[:-1]

        array_2 = company_tag_given.split("|")

        company_tag_given_b1 = array_2[0]

        company_tag_given_b2 = array_2[1]

        # if company_tag_given == "||":
        #     company_tag_given = ""

        if not document["OriginalDateOfContract"]:
            time_tag = "U"
        else:
            if document["OriginalDateOfContract"] < 20130000:
                time_tag = "O"

        if (document["ResidentialIndicator"] and document["ResidentialIndicator"] == 1) or (
                document["PropertyUseCode"] and document["PropertyUseCode"].strip() in propertyUseCodeList):
            residential_tag = 1

        # Prepare update data for each document
        update_operation = UpdateOne(
            {"_id": document["_id"]},
            {"$set": {"company_tag_cal_b1": company_tag_cal_b1, "company_tag_cal_b2": company_tag_cal_b2,
                      "time_tag": time_tag, "company_tag_given_b1": company_tag_given_b1,
                      "company_tag_given_b2": company_tag_given_b2, "residential_tag": residential_tag}}
            # {"$set": {"time_tag": time_tag}}
        )

        last_processed_id = document["_id"]

        update_operations.append(update_operation)

    if update_operations:
        collection_sam.bulk_write(update_operations)

et = get_current_time()
duration = et - st

print(f"Processing time for update time_tag, residential_tag and company_tag table: {duration} seconds")

# Close the MongoDB connection
client.close()
