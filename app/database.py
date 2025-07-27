from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

# Example collections
user_collection = db.get_collection("users")
sweet_collection = db.get_collection("sweets")