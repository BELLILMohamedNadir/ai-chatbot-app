from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.chat import ChatSession, ChatMessage
from ..schemas.chat import ChatSessionCreate, ChatMessageCreate


class CRUDChatSession:
    def get(self, db: Session, id: int) -> Optional[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.id == id).first()
    
    def get_by_room_id(self, db: Session, room_id: str) -> Optional[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.room_id == room_id).first()
    
    def get_user_sessions(self, db: Session, user_id: int) -> List[ChatSession]:
        """Get all chat sessions (rooms) for a user"""
        return db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.updated_at.desc()).all()
    
    def create(self, db: Session, user_id: int, room_id: str) -> ChatSession:
        db_obj = ChatSession(user_id=user_id, room_id=room_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        obj = db.query(ChatSession).filter(ChatSession.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False


class CRUDChatMessage:
    def create(self, db: Session, obj_in: ChatMessageCreate) -> ChatMessage:
        db_obj = ChatMessage(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_session_messages(self, db: Session, session_id: int) -> List[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()


chat_session = CRUDChatSession()
chat_message = CRUDChatMessage()
