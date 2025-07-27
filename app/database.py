from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# Initialize MongoDB client using the configured URI
client = AsyncIOMotorClient(settings.MONGO_URI)

# Access the database specified in settings
db = client[settings.DB_NAME]

# Define collections for users and sweets
user_collection = db.get_collection("users")
sweet_collection = db.get_collection("sweets")
