"""Load generated transactions into MongoDB using PyMongo."""
import os
import pandas as pd
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB = os.getenv("MONGODB_DB", "fintech_fraud")
COLLECTION = os.getenv("MONGODB_COLLECTION", "transactions")

def main():
    df = pd.read_csv("transactions.csv")
    docs = df.to_dict(orient="records")
    client = MongoClient(URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    col = client[DB][COLLECTION]
    col.delete_many({})
    if docs:
        for start in range(0, len(docs), 1000):
            col.insert_many(docs[start:start+1000], ordered=False)
    col.create_index([("transaction_id", ASCENDING)], unique=True)
    col.create_index([("customer_id", ASCENDING)])
    col.create_index([("is_fraud", ASCENDING)])
    print(f"Inserted {col.count_documents({}):,} records into {DB}.{COLLECTION}")
    client.close()

if __name__ == "__main__":
    main()
