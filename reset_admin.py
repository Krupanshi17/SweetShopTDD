import bcrypt
from pymongo import MongoClient
from bson.binary import Binary, UuidRepresentation
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "sweetshop_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users = db.users

email = "admin@example.com"
password = "AdminSecret123"
role = "admin"

# Delete existing admin user if exists
users.delete_many({"email": email})

# Hash the password
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Insert new admin user with correct UUID BSON encoding
admin_user = {
    "_id": Binary.from_uuid(uuid.uuid4(), uuid_representation=UuidRepresentation.STANDARD),
    "email": email,
    "hashed_password": hashed_password.decode('utf-8'),
    "role": role
}

users.insert_one(admin_user)

print("Admin user reset successfully!")
