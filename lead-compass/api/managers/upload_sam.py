from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from data import load_json

_ = load_dotenv(find_dotenv())
# mongo_url = os.getenv("MONGO_URL")

client = MongoClient("mongodb://localhost:27017")
db = client["lead_compass"]
sam_collection = db["complete_sam"]

companies = load_json.company_data

result_sam = sam_collection.insert_many(companies)
total_docs = len(result_sam.inserted_ids)
print(f"sam table uploaded with {total_docs}")

