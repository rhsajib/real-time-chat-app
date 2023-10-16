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