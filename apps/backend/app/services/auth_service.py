from sqlalchemy.orm import Session
from ..crud.user import user as user_crud
from ..schemas.user import UserCreate
from ..core.security import create_access_token, verify_token
from datetime import timedelta
from ..core.config import settings


class AuthService:
    def authenticate_user(self, db: Session, email: str, password: str):
        """Authenticate user by email and password."""
        return user_crud.authenticate(db, email=email, password=password)
    
    def create_user(self, db: Session, user_in: UserCreate):
        """Create new user."""
        return user_crud.create(db, obj_in=user_in)
    
    def create_access_token_for_user(self, user):
        """Create JWT access token for user."""
        token_data = {"sub": str(user.id), "email": user.email}
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(data=token_data, expires_delta=access_token_expires)
    
    def get_current_user(self, db: Session, token: str):
        """Get current user from JWT token."""
        payload = verify_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = user_crud.get(db, id=int(user_id))
        return user


auth_service = AuthService()
