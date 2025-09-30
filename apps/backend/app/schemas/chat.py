from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatMessageBase(BaseModel):
    content: str
    sender: str  # 'user' or 'ai'


class ChatMessageCreate(ChatMessageBase):
    session_id: int
    model: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time_ms: Optional[float] = None


class ChatMessage(ChatMessageBase):
    id: int
    session_id: int
    model: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time_ms: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    model: str = "mistral-small-latest"
    temperature: float = 0.7


class ChatResponse(BaseModel):
    response: str
    model: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time_ms: Optional[float] = None


class ChatSessionCreate(BaseModel):
    room_id: str


class ChatSession(BaseModel):
    id: int
    user_id: int
    room_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
