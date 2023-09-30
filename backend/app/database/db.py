from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
# import logging



# MongoDB connection URL
MONGODB_URL = f'mongodb://{settings.HOST}:{settings.PORT}'

# Create an AsyncIOMotorClient for MongoDB
mongo_client = AsyncIOMotorClient(MONGODB_URL)

# Create a reference to the MongoDB database
mongo_db = mongo_client[settings.DB_NAME]


# Dependency to get the MongoDB database
def get_mongo_db():
    try:
        yield mongo_db
    finally:
        mongo_client.close()


# Send a ping to confirm a successful connection
try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You have successfully connected to MongoDB!")
except Exception as e:
    print(e)
        

