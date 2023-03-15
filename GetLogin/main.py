from datetime import datetime 

import time
import pymongo
import os
from dotenv import load_dotenv

from module.authy import authy
from module.driver import driver

# Load environment variables from .env file
load_dotenv()
mongo_client_link = os.getenv('MONGO_CLIENT_LINK')
mongo_client_db = os.getenv('MONGO_CLIENT_DB')
mongo_client_collection = os.getenv('MONGO_CLIENT_COLLECTION')
try:
    mongo_client = pymongo.MongoClient(mongo_client_link)
    mongo_client.server_info()
    print("Database connected!")
except Exception as err:
    print("Database connected error!")
    exit()

manual_timer = 80

# Get Username & Password
username, password, fill_password = authy()

# Web Driver get Cookies
hoyolab_cookies = driver(username, password, fill_password)

# Access GenshinTest database
hoyolab_db = mongo_client[mongo_client_db]
users_collection = hoyolab_db[mongo_client_collection]

# check if user with entered username already exists in the database
existing_user = users_collection.find_one({"username": username})
if existing_user:
    # update the existing user's cookies
    users_collection.update_one({"_id": existing_user["_id"]}, {"$set": {"cookies": hoyolab_cookies, 'timestamp': datetime.now()}})
    print(f"User {username}'s cookies updated in MongoDB")
else:
    # insert a new user with the entered username and extracted cookies
    user_data = {"username": username, "cookies": hoyolab_cookies, 'timestamp': datetime.now()}
    users_collection.insert_one(user_data)
    print(f"New user {username} and cookies saved to MongoDB")


