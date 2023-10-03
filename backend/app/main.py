from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import user_router, chat_router
from app.database.db import (
    startup_db_client,
    shutdown_db_client,
    db_connection_status,
)


app = FastAPI()


# Register the startup event handler
@app.on_event('startup')
async def startup_event():
    await startup_db_client(app)
    await db_connection_status()


# Register the shutdown event handler
@app.on_event('shutdown')
async def shutdown_event():
    await shutdown_db_client(app)


origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# App root
@app.get('/', tags=['Root'])
async def root():
    return {'message': 'Welcome to this fantastic app!'}


# Routers
app.include_router(user_router.router, tags=['User'], prefix='/api/v1/user')
app.include_router(chat_router.router, tags=['Chat'], prefix='/api/v1/chat')
