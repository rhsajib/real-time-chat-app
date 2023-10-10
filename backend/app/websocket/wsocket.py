import json
from fastapi import WebSocket, WebSocketDisconnect

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.crud.chat import db_create_message
from app.database.db import get_db
from app.serializers.serializers import new_message_serializer

# Store connected WebSocket clients
connected_clients: dict[str, set] = dict()


async def chat_websocket_endpoint(chat_id: str,
                                  websocket: WebSocket,
                                  db: AsyncIOMotorDatabase = Depends(get_db)):
    await websocket.accept()
    print(f"WebSocket connection established for chat id: {chat_id}.")

    # Add the WebSocket to the set of connected clients
    if chat_id in connected_clients:
        connected_clients[chat_id].add(websocket)
    else:
        connected_clients[chat_id] = {websocket}
    print('connected_clients', connected_clients)

    try:
        while True:
            message = await websocket.receive_text()
            print("Message received:", message)

            # Handle incoming messages
            current_user_id = '2123bb0ec29d4471bd295be4cca68aed'  # user2
        
            new_message = await db_create_message(current_user_id, chat_id, message, db)

            # in serialized_message date time is converted to string
            serialized_message = new_message_serializer(new_message)

            # # Convert the serialized_message to JSON format
            message_response = serialized_message.model_dump()
            print('message_response', message_response)

            # Broadcast the message to all connected clients
            for client_ws in connected_clients[chat_id]:
                print('client_ws', client_ws)
                await client_ws.send_json(message_response)

    except WebSocketDisconnect:
        print("WebSocket connection closed.")

    finally:
        # Remove disconnected client from the set
        print(f'Removed disconnected client websocket: {websocket} from the Chat id: {chat_id}')
        # handle removing clients
        connected_clients[chat_id].remove(websocket)

        # handle removing chat_id from connected_clients if no clints are connected
        if len(connected_clients[chat_id]) == 0:
            del connected_clients[chat_id]
            print(f'Removed chat id: {chat_id} as there are no clints.')
        print('Finally remaining clints:', connected_clients)
