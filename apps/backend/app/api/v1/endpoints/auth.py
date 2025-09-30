from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....db.database import get_db
from ....services.auth_service import auth_service
from ....schemas.auth import Token, LoginRequest
from ....schemas.user import User, UserCreate
from ....crud.user import user as user_crud
from ....api.deps import get_current_active_user

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """Register new user"""
    # Check if email already exists
    existing_user = user_crud.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists"
        )
    
    # Check if username already exists
    existing_username = user_crud.get_by_username(db, username=user_in.username)
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists"
        )
    
    user = auth_service.create_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user and return access token"""
    user = auth_service.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token_for_user(user)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=User)
def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user info"""
    return current_user
