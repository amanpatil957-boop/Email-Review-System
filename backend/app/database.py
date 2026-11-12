
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from backend/.env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

# Get MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is missing from backend/.env")

# Connect to MongoDB Atlas
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

# Select database and collection
db = client["mailmind_db"]
emails_collection = db["emails"]


def check_database_connection():
    try:
        client.admin.command("ping")
        print("MongoDB Atlas Connected Successfully!")
        return True

    except Exception as error:
        print("MongoDB Connection Failed:", error)
        return False
