import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
print(f"Connecting to MongoDB at {MONGODB_URI}...")

try:
    client = MongoClient(MONGODB_URI)
    db = client["lgs_soru_tahmin"]
    user_count = db.users.count_documents({})
    pred_count = db.predictions.count_documents({})
    print(f"Users in DB: {user_count}")
    print(f"Predictions in DB: {pred_count}")

    if user_count > 0:
        # Get a sample user
        user = db.users.find_one()
        username = user.get("username")
        print(f"Testing API for username: {username}")

        # Test API
        try:
            r = requests.get(f"http://localhost:8000/api/profil/son-cozulen-sorular", params={"username": username})
            print(f"API Status: {r.status_code}")
            if r.status_code == 200:
                print("API Response:", r.json())
            else:
                print("API Error Response:", r.text)
        except Exception as e:
            print(f"API Connection Failed: {e}")

    else:
        print("No users found to test API with.")

except Exception as e:
    print(f"MongoDB Failed: {e}")
