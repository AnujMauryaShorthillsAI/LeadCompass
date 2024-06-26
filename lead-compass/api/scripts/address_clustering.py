import os
import time
import json
import sys
import pandas as pd
import networkx as nx
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
 
class JSONEncoder(json.JSONEncoder):  
    def default(self, o):  
        if isinstance(o, ObjectId):  
            return str(o)  
        return json.JSONEncoder.default(self, o)  
 
 
DB_NAME = "lead_compass"
 
def get_db_client():
    load_dotenv()
    MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")
    client = MongoClient("mongodb://localhost:27017")
    return client
 
def get_db(client, db_name):
    return client[db_name]
 
def get_current_time():
    return time.time()
 
# Get the starting time
st = get_current_time()
 
with get_db_client() as client:
    db = get_db(client ,DB_NAME)
    SOURCE = sys.argv[1]
    TARGET = sys.argv[2]
    PROJECT_ID = sys.argv[3]

    # SOURCE = "test_filtered_borrowers"
    # TARGET = "test_borrowers_cluster"
    # PROJECT_ID = "65a3ff7be0d06b46084ef135"

    source_collection = db[SOURCE]
 
    projected_fields = {"LC_Borrower": 1, "LC_TotalLoanAmount": 1, "LC_NumberOfLoans": 1, "LC_BorrowerFullAddressJsonSet": 1, "LC_LatestTransactionDate": 1, "LC_TotalNumberOfPropertyTransactions": 1, "_id": 1, "LC_BorrowerFullAddressSet":1, "ProjectId": 1 }
    
    project_id = PROJECT_ID
    # Fetch all documents from the collection
    cursor = source_collection.find({"ProjectId":project_id}, projected_fields)
    # cursor = source_collection.find({}, projected_fields)

    df = pd.DataFrame(list(cursor))
 
    unique_mail_addresses_list = []
    map = {}
 
    # Iterate through the rows of the dataframe
    for index, row in df.iterrows():
        address_list = row['LC_BorrowerFullAddressSet']
        address_list = [item for item in address_list if item is not None]
 
        for address in address_list:
            if address not in map:
                unique_mail_addresses_list.append(address)
                map[address] = {"LC_BorrowersList": [row['LC_Borrower']]}
            else:
                map[address]["LC_BorrowersList"].append(row['LC_Borrower'])
 
    print("Done creating address borrowers map")
 
    # Create a DSU object with number of unique mail addresses as parameter
    graph = nx.Graph()
    graph.add_nodes_from(unique_mail_addresses_list)
 
    # Iterate through the rows of the dataframe
    for index, row in df.iterrows():
        address_list_large = row['LC_BorrowerFullAddressSet']
        address_list_large = [item for item in address_list_large if item is not None]
 
        for address_nth in address_list_large[1:]:
            graph.add_edge(address_list_large[0], address_nth)
 
    # Use connected components to find clusters
    clusters = list(nx.connected_components(graph))
 
    print("Done graph clustering moving on other things")
    print(f"Total clusters created is {len(clusters)}")
 
    res_list = []
 
 
    print("Started created index for data Frame")
 
    df.set_index('LC_Borrower', inplace=True)  
 
    print("Created index for the dataframe for field LC_Borrower")
  
    for i, cluster in enumerate(clusters):
        if i % 5000 == 0:
            print(i)
    
        borrowers_set = set()
        for address in cluster:  
            borrowers_set.update(map[address]["LC_BorrowersList"])  
            
        # df_filtered = df[df['LC_Borrower'].isin(borrowers_set)]  
        df_filtered = df.loc[df.index.isin(borrowers_set)]  
        
        # borrowers_metadata = df_filtered[['LC_Borrower', 'LC_TotalLoanAmount', 'LC_NumberOfLoans', 'LC_BorrowerFullAddressSet', 'LC_BorrowerFullAddressJsonSet', 'LC_LatestTransactionDate', 'LC_TotalNumberOfPropertyTransactions', '_id']].set_index('LC_Borrower').to_dict('index')
        borrowers_metadata = df_filtered[['LC_TotalLoanAmount', 'LC_NumberOfLoans', 'LC_BorrowerFullAddressSet', 'LC_BorrowerFullAddressJsonSet', 'LC_LatestTransactionDate', 'LC_TotalNumberOfPropertyTransactions', '_id', 'ProjectId']].to_dict('index')
 
        borrower_dpid_counts = {}    
        for borrower, metadata in borrowers_metadata.items():    
            borrower_dpid_counts[borrower] = metadata["LC_TotalNumberOfPropertyTransactions"]    
    
        LC_ParentSponsor = max(borrower_dpid_counts, key=borrower_dpid_counts.get)  
    
        borrowers_metadata_list = [{"LC_Borrower": k, **v} for k, v in borrowers_metadata.items()]  
    
        res_list.append({"LC_ParentSponsor": LC_ParentSponsor, "LC_BorrowerMetaData": borrowers_metadata_list, "LC_FilterUsed": "MaxPropertyTransaction", "LC_DateOfParentCreation": datetime.now().strftime('%Y%m%d'),"ProjectId": project_id })  
    
 
    print("Done creating list for final insertion")
 
    # with open('data.json', 'w') as f:  
    #     f.write(JSONEncoder().encode(res_list)) 
     
    target_collection = db[TARGET]
    target_collection.insert_many(res_list)
 
    print("Done dumping data into a json file")
 
    # Get the end time
    et = get_current_time()
 
    print(f"Total time  taken in the whole process is {et-st} seconds")