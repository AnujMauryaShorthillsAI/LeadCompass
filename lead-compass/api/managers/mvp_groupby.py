from pymongo import MongoClient, WriteConcern
import os, time, sys
from dotenv import load_dotenv
import pandas as pd
from pymongo import UpdateOne

load_dotenv()

DB_NAME = "lead_compass"

# MONGO_CONNECTION_URL = os.getenv("mongodb://localhost:27017")

client = MongoClient("mongodb://localhost:27017")

# Access a specific database (replace 'your_database' with your actual database name)
db = client[DB_NAME]
collection_project = db["project"]

source_collection_name = "mvp"
target_collection_name = "group_mvp"

source_collection = db[source_collection_name]
collection_mvp_group = db["group_mvp"]


def get_current_time():
    return time.time()


st = get_current_time()

latest_project = collection_project.find_one({}, sort=[("_id", -1)])
latest_project_id = latest_project.get("project_id", 0)

# Define your filter criteria
filter_criteria = {"ProjectId": latest_project_id}

# update_statement = {
#     "$set": {"projectID": latest_project_id}
# }
#
# # Perform the update using the filter criteria
# collection_mvp_group.update_one(filter_criteria, update_statement)

cursor = source_collection.find(filter_criteria).limit(5000)

data = list(cursor)

client.close()

print("Done loading data")

df = pd.DataFrame(data)

df = df.drop('_id', axis=1)


def map_to_dict(x):
    return dict(map(lambda item: (str(item[0]), item[1]), x.value_counts().to_dict().items()))


# Group by 'Borrower' and perform aggregation
grouped_df = df.groupby('RcCalBorrower').agg(
    ProjectId=('ProjectId', 'first'),
    RcCalTotalLoanAmount=('RcCalPartialLoanAmount', 'sum'),
    RcCalNumberOfLoans=('RcCalBorrower', 'count'),

    PropertyFullStreetAddress=('PropertyFullStreetAddress', map_to_dict),
    PropertyState=('PropertyState', map_to_dict),
    PropertyCityName=('PropertyCityName', map_to_dict),

    PropertyZipCode=('PropertyZipCode', map_to_dict),
    PropertyZip4=('PropertyZip4', map_to_dict),
    PropertyUnitType=('PropertyUnitType', map_to_dict),
    PropertyUnitNumber=('PropertyUnitNumber', map_to_dict),

    BuyerMailFullStreetAddress=('BuyerMailFullStreetAddress', map_to_dict),
    BuyerMailCity=('BuyerMailCity', map_to_dict),
    BuyerMailState=('BuyerMailState', map_to_dict),

    BuyerMailZipCode=('BuyerMailZipCode', map_to_dict),
    BuyerMailZip4=('BuyerMailZip4', map_to_dict),
    BuyerMailUnitType=('BuyerMailUnitType', map_to_dict),
    BuyerMailUnitNumber=('BuyerMailUnitNumber', map_to_dict),

    RcCalType=('RcCalType', map_to_dict),
    DPID=('DPID', map_to_dict),

    RcCalSource=('RcCalSource', map_to_dict),
    OriginalDateOfContract=('OriginalDateOfContract', map_to_dict),
    LenderNameBeneficiary=('LenderNameBeneficiary', map_to_dict),
    RcCalLatestTransactionDate=('OriginalDateOfContract', 'max'),

).reset_index()

print("Done initial group BY")

# Aggregate transactions into a list for each borrower
grouped_df['RcCalTransactions'] = \
    df.groupby('RcCalBorrower').apply(lambda x: x.drop('RcCalBorrower', axis=1).to_dict(orient='records')).reset_index(
        name='RcCalTransactions')['RcCalTransactions']

print("Done 2nd group BY")

# Dump the resulting DataFrame into a new MongoDB collection

output_data = grouped_df.to_dict(orient='records')

client = MongoClient("mongodb://localhost:27017")

# Access a specific database (replace 'your_database' with your actual database name)
db = client[DB_NAME]

target_collection = db[target_collection_name]

# Set the batch size for the insert operation
batch_size = 500

size_borrowers = len(output_data)

# Insert the data in batches
for i in range(0, size_borrowers, batch_size):
    print(f"Uploaded {i} till now")
    batch = output_data[i:i + batch_size]
    target_collection.insert_many(batch)

print("Done uploading")

et = get_current_time()

print(f"Time taken {et - st}")

# Close the MongoDB connection
client.close()
