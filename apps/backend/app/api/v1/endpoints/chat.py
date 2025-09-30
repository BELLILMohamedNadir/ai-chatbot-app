from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....db.database import get_db
from ...deps import get_current_active_user
from ....services.ai_service import ai_service
from ....models.user import User
from ....schemas.chat import ChatRequest, ChatResponse, ChatSession, ChatSessionCreate
from ....crud.chat import chat_session

router = APIRouter()


@router.get("/rooms", response_model=List[ChatSession])
def get_all_rooms(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all chat rooms (sessions) for current user"""
    rooms = chat_session.get_user_sessions(db, user_id=current_user.id)
    return rooms


@router.post("/rooms", response_model=ChatSession, status_code=201)
def create_room(
    room_data: ChatSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new chat room (session)"""
    # Check if room already exists
    existing_room = chat_session.get_by_room_id(db, room_id=room_data.room_id)
    if existing_room:
        raise HTTPException(status_code=400, detail="Room with this ID already exists")
    
    new_room = chat_session.create(db, user_id=current_user.id, room_id=room_data.room_id)
    return new_room


@router.delete("/rooms/{room_id}", status_code=204)
def delete_room(
    room_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a chat room (session)"""
    room = chat_session.get_by_room_id(db, room_id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this room")
    
    chat_session.delete(db, id=room.id)
    return None


@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Send message to AI and get response"""
    try:
        # Generate AI response
        ai_response = await ai_service.generate_response(
            message=chat_request.message,
            model=chat_request.model,
            temperature=chat_request.temperature
        )
        
        return ChatResponse(**ai_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
