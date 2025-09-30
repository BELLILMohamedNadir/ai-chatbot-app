"""
Database seeding script for AI Chatbot application
"""
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models.user import User
from app.models.chat_room import ChatRoom, RoomMember, RoomType
from app.models.message import Message, MessageRole, MessageStatus
from app.core.security import get_password_hash
from app.utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def create_sample_data():
    """Create sample data for development and testing"""
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            logger.info("Sample data already exists, skipping...")
            return
        
        logger.info("Creating sample data...")
        
        # Create sample users
        users = [
            User(
                email="alice@example.com",
                username="alice",
                full_name="Alice Johnson",
                hashed_password=get_password_hash("password123"),
                is_active=True,
                is_verified=True
            ),
            User(
                email="bob@example.com",
                username="bob",
                full_name="Bob Smith",
                hashed_password=get_password_hash("password123"),
                is_active=True,
                is_verified=True
            ),
            User(
                email="charlie@example.com",
                username="charlie",
                full_name="Charlie Brown",
                hashed_password=get_password_hash("password123"),
                is_active=True,
                is_verified=True
            ),
            User(
                email="demo@example.com",
                username="demo",
                full_name="Demo User",
                hashed_password=get_password_hash("demo123"),
                is_active=True,
                is_verified=True
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        logger.info(f"Created {len(users)} sample users")
        
        # Create sample chat rooms
        rooms = [
            ChatRoom(
                name="General Discussion",
                description="A place for general conversation",
                room_type=RoomType.PUBLIC,
                max_members=100,
                owner_id=users[0].id
            ),
            ChatRoom(
                name="Tech Talk",
                description="Discuss technology and programming",
                room_type=RoomType.PUBLIC,
                max_members=50,
                owner_id=users[1].id
            ),
            ChatRoom(
                name="Random",
                description="Random topics and fun conversations",
                room_type=RoomType.PUBLIC,
                max_members=75,
                owner_id=users[2].id
            ),
            ChatRoom(
                name="AI Enthusiasts",
                description="Discuss AI, ML, and the future of technology",
                room_type=RoomType.PUBLIC,
                max_members=200,
                owner_id=users[3].id
            )
        ]
        
        for room in rooms:
            db.add(room)
        
        db.commit()
        logger.info(f"Created {len(rooms)} sample rooms")
        
        # Add room memberships
        memberships = []
        
        # Add owners as admins
        for i, room in enumerate(rooms):
            membership = RoomMember(
                room_id=room.id,
                user_id=room.owner_id,
                is_admin=True
            )
            memberships.append(membership)
        
        # Add other users to rooms
        for user in users:
            for room in rooms:
                if room.owner_id != user.id:  # Don't duplicate owner membership
                    membership = RoomMember(
                        room_id=room.id,
                        user_id=user.id,
                        is_admin=False
                    )
                    memberships.append(membership)
        
        for membership in memberships:
            db.add(membership)
        
        db.commit()
        logger.info(f"Created {len(memberships)} room memberships")
        
        # Create sample messages
        sample_messages = [
            # General Discussion
            {
                "room_id": rooms[0].id,
                "user_id": users[0].id,
                "content": "Welcome to the General Discussion room! Feel free to chat about anything here.",
                "role": MessageRole.USER
            },
            {
                "room_id": rooms[0].id,
                "user_id": users[1].id,
                "content": "Thanks Alice! This is a great space for conversations.",
                "role": MessageRole.USER
            },
            {
                "room_id": rooms[0].id,
                "user_id": None,  # AI message
                "content": "Hello everyone! I'm the AI assistant. Feel free to ask me anything or just chat!",
                "role": MessageRole.ASSISTANT,
                "model_name": "mistral-small-latest"
            },
            
            # Tech Talk
            {
                "room_id": rooms[1].id,
                "user_id": users[1].id,
                "content": "What's everyone working on lately? I've been exploring FastAPI for building APIs.",
                "role": MessageRole.USER
            },
            {
                "room_id": rooms[1].id,
                "user_id": users[2].id,
                "content": "FastAPI is amazing! The automatic documentation and type hints make development so much smoother.",
                "role": MessageRole.USER
            },
            
            # AI Enthusiasts
            {
                "room_id": rooms[3].id,
                "user_id": users[3].id,
                "content": "Has anyone tried the latest language models? The improvements in reasoning are incredible.",
                "role": MessageRole.USER
            },
            {
                "room_id": rooms[3].id,
                "user_id": None,  # AI message
                "content": "I'm excited to be part of this discussion! Language models have indeed made significant progress in recent years. What specific aspects of reasoning improvements have you noticed?",
                "role": MessageRole.ASSISTANT,
                "model_name": "mistral-small-latest"
            }
        ]
        
        messages = []
        for msg_data in sample_messages:
            message = Message(
                room_id=msg_data["room_id"],
                user_id=msg_data.get("user_id"),
                role=msg_data["role"],
                content=msg_data["content"],
                status=MessageStatus.SENT,
                model_name=msg_data.get("model_name"),
                sentiment_score=0.1 if "great" in msg_data["content"].lower() else 0.0,
                sentiment_label="neutral"
            )
            messages.append(message)
        
        for message in messages:
            db.add(message)
        
        db.commit()
        logger.info(f"Created {len(messages)} sample messages")
        
        logger.info("Sample data creation completed successfully!")
        
        # Print login credentials
        print("\n" + "="*50)
        print("SAMPLE USER CREDENTIALS")
        print("="*50)
        print("Email: alice@example.com | Password: password123")
        print("Email: bob@example.com   | Password: password123") 
        print("Email: charlie@example.com | Password: password123")
        print("Email: demo@example.com  | Password: demo123")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
