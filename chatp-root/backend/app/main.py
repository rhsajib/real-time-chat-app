from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

from app.core.config import settings
from app.websocket.wsocket import chat_websocket_endpoint
from app.database.db import (
    startup_db_client,
    shutdown_db_client,
    db_connection_status,
)

from fastapi.routing import APIWebSocketRoute


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




app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# App root
@app.get('/', tags=['Root'])
async def root():
    return {'message': 'Welcome to this fantastic ChatP app!'}


# Api Routers
app.include_router(api_router, prefix=settings.API_V1_STR)


# Register the WebSocket endpoint
app.router.routes.append(APIWebSocketRoute('/ws/chat/{chat_type}/{chat_id}/token={token}', chat_websocket_endpoint))

# routes = [WebSocketRoute(path, endpoint=...), ...]
# app = Starlette(routes=routes)

 

"""

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from socketio import AsyncServer

app = FastAPI()

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

sio = AsyncServer(async_mode="asgi", cors_allowed_origins=origins)
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")

@sio.on("chat_message")
async def handle_chat_message(sid, data):
    # Handle the chat message and broadcast it to all clients
    await sio.emit("chat_message", data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
