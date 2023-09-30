from fastapi import FastAPI
from app.database.db import mongo_client, mongo_db



app = FastAPI()

# Startup event handler for MongoDB
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = mongo_client
    app.mongodb = mongo_db


# Shutdown event handler for MongoDB
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get('/')
async def root():
    return({'message': 'Hello World'})