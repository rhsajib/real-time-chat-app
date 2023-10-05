from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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


# Store connected WebSocket clients
connected_clients = set()

# WebSocket endpoint to handle connections


@app.websocket('/ws/chat/{client_id}')
async def websocket_endpoint(client_id: str, websocket: WebSocket):
    await websocket.accept()
    print(f"WebSocket connection established for client {client_id}.")

    # Add the WebSocket to the set of connected clients
    connected_clients.add((client_id, websocket))

    print(connected_clients)

    try:
        while True:
            data = await websocket.receive_text()
            print("Message received:", data)

            # Handle incoming messages here
            # ............................
            # ............................
            # ............................

            # Broadcast the message to all connected clients
            for client in connected_clients:
                client_id, client_ws = client
                print('client_ws', client_ws)
                await client_ws.send_text(data)

    except WebSocketDisconnect:
        print("WebSocket connection closed.")

    finally:
        # Remove disconnected client from the set
        print(
            f'Remove disconnected client from the set {client_id}, {websocket}')
        connected_clients.remove((client_id, websocket))
        print(connected_clients)


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
