
import os
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
# import logging


# Determine the MongoDB URL based on the environment (Docker or local)
if "MONGODB_URI" in os.environ:
    MONGODB_URL = os.environ["MONGODB_URI"]
else:
    # MongoDB connection URL for local machine
    MONGODB_URL = f'mongodb://{settings.HOST}:{settings.PORT}'

# Create an AsyncIOMotorClient for MongoDB
mongo_client = AsyncIOMotorClient(MONGODB_URL)

# Create a reference to the MongoDB database
mongo_db = mongo_client[settings.DB_NAME]


# Dependency to get the MongoDB database
async def get_db() -> AsyncIOMotorDatabase:
    try:
        yield mongo_db
    finally:
        # Here we don't need to close the database in the dependency.
        # Closing should be handled in the shutdown event handler.
        pass


# Define an asynchronous function to ping the MongoDB server
async def ping_mongodb():
    try:
        await mongo_client.admin.command('ping')
        print("Connection status: You have successfully connected to MongoDB!")
    except Exception as e:
        print(e)


# Asynchronously execute the ping operation
async def db_connection_status():
    await ping_mongodb()


# Define the startup event handler for MongoDB
async def startup_db_client(app):
    app.mongodb_client = mongo_client
    app.mongodb = mongo_db

# Define the shutdown event handler for MongoDB


async def shutdown_db_client(app):
    app.mongodb_client.close()


# Define an asynchronous function to check the MongoDB connection status
async def db_connection_status():
    await ping_mongodb()
