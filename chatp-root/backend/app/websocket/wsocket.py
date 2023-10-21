from fastapi import WebSocket, WebSocketDisconnect, Depends
from app import schemas
from app.api.v1.dependencies import (
    get_group_chat_manager, 
    get_private_chat_manager,
    get_token_manager,
    get_user_manager
)
from app.core.config import settings
from app.services.token import TokenManager
from app.crud.chat import GroupChatManager, PrivateChatManager
from app.crud.user import User
from app.serializers.serializers import message_serializer

# Store connected WebSocket clients
connected_clients: dict[str, set] = dict()


async def chat_websocket_endpoint(
    chat_type: str,
    chat_id: str,
    token: str,
    websocket: WebSocket,
    token_subject_key:str =settings.ACCESS_TOKEN_SUBJECT_KEY,
    token_manager:  TokenManager = Depends(get_token_manager),
    pvt_chat_manager: PrivateChatManager = Depends(get_private_chat_manager),
    # grp_chat_manager: GroupChatManager = Depends(get_group_chat_manager),
    
):
    """
        current_user: schemas.User = Depends(get_current_active_user)
        we can't use it because get_current_active_user depends on oauth2_scheme
        which is an instance of OAuth2PasswordBearer.

        OAuth2PasswordBearer does require a Request argument to 
        extract the token from the request. However, when working with 
        WebSocket connections, we won't have access to the request object 
        in the same way you do with HTTP requests.

        so we have to use another technique to retrieve 
        current_user more specifically access-token.

        Thats why we created a TokenManager to reuse it in http request
        as well as in websocket

    """
    await websocket.accept()
    print(f"WebSocket connection established for chat id: {chat_id}.")

    # get current user
    current_user = await token_manager.get_user_form_jwt_token(token, token_subject_key)
    print('current_user for websocket', 
          'username', current_user['username'], 
          'id', current_user['id'])

    # Add the WebSocket to the set of connected clients
    if chat_id in connected_clients:
        connected_clients[chat_id].add(websocket)
    else:
        connected_clients[chat_id] = {websocket}
    print('connected_clients', connected_clients)

    try:
        while True:

            message = await websocket.receive_text()
            # print("Message received:", message)


            # Handle incoming messages
            if chat_type == 'private':
                new_message = await pvt_chat_manager.create_message(current_user['id'], chat_id, message)
            # elif chat_type == 'group':
            #     new_message = await grp_chat_manager.create_message(current_user['id'], chat_id, message)


            # in serialized_message date time is converted to string
            serialized_message = message_serializer(new_message.model_dump())
            print('message_response', serialized_message)

            # Broadcast the message to all connected clients
            for client_ws in connected_clients[chat_id]:
                print('client_ws', client_ws)
                await client_ws.send_json(serialized_message)

    except WebSocketDisconnect:
        print("WebSocket connection closed.")

    finally:
        # Remove disconnected client from the set
        print(
            f'Removed disconnected client websocket: {websocket} from the Chat id: {chat_id}')
        # handle removing clients
        connected_clients[chat_id].remove(websocket)

        # handle removing chat_id from connected_clients if no clints are connected
        if len(connected_clients[chat_id]) == 0:
            del connected_clients[chat_id]
            print(f'Removed chat id: {chat_id} as there are no clints.')
        print('Finally remaining clints:', connected_clients)
