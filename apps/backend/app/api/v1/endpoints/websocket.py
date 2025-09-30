from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import json
from datetime import datetime

from ....db.database import get_db
from ....core.websocket_manager import manager
from ....core.security import verify_token
from ....crud.user import user as user_crud
from ....crud.chat import chat_session, chat_message
from ....schemas.chat import ChatMessageCreate
from ....services.ai_service import ai_service

router = APIRouter()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time chat"""
    
    # Verify token
    if not token:
        await websocket.close(code=4001, reason="Missing token")
        return
    
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=4001, reason="Invalid token")
        return
    
    user_id = payload.get("sub")
    if not user_id:
        await websocket.close(code=4001, reason="Invalid token payload")
        return
    
    # Get user
    user = user_crud.get(db, id=int(user_id))
    if not user:
        await websocket.close(code=4001, reason="User not found")
        return
    
    # Get or create chat session
    session = chat_session.get_by_room_id(db, room_id=room_id)
    if not session:
        session = chat_session.create(db, user_id=user.id, room_id=room_id)
    
    # Connect to room
    await manager.connect(websocket, room_id)
    
    try:
        # Send welcome message
        await manager.send_personal_message(
            json.dumps({
                "type": "system",
                "message": f"Connected to room: {room_id}",
                "timestamp": datetime.utcnow().isoformat()
            }),
            websocket
        )
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            model = message_data.get("model", "mistral-small-latest")
            temperature = message_data.get("temperature", 0.7)
            
            # Save user message to database
            user_msg = ChatMessageCreate(
                session_id=session.id,
                content=user_message,
                sender="user"
            )
            chat_message.create(db, obj_in=user_msg)
            
            # Broadcast user message to room
            await manager.broadcast_to_room({
                "type": "user",
                "message": user_message,
                "username": user.username,
                "timestamp": datetime.utcnow().isoformat()
            }, room_id)
            
            # Generate AI response
            try:
                ai_response = await ai_service.generate_response(
                    message=user_message,
                    model=model,
                    temperature=temperature
                )
                
                # Save AI message to database
                ai_msg = ChatMessageCreate(
                    session_id=session.id,
                    content=ai_response["response"],
                    sender="ai",
                    model=model,
                    tokens_used=ai_response.get("tokens_used"),
                    response_time_ms=ai_response.get("response_time_ms")
                )
                chat_message.create(db, obj_in=ai_msg)
                
                # Broadcast AI response to room
                await manager.broadcast_to_room({
                    "type": "ai",
                    "message": ai_response["response"],
                    "model": model,
                    "timestamp": datetime.utcnow().isoformat()
                }, room_id)
                
            except Exception as e:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": f"AI error: {str(e)}",
                        "timestamp": datetime.utcnow().isoformat()
                    }),
                    websocket
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast_to_room({
            "type": "system",
            "message": f"User {user.username} left the room",
            "timestamp": datetime.utcnow().isoformat()
        }, room_id)
