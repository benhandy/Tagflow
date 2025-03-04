from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User
from auth.jwt import create_access_token, create_refresh_token
from auth.config import Token
from utils.security import verify_password
from exceptions.auth import InvalidCredentialsError, TokenExpiredError
from schemas.error import ErrorResponse

router = APIRouter(tags=["auth"])

@router.post("/token", 
    response_model=Token,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsError()
    
    # Create tokens
    access_token = create_access_token({"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    access_token = create_access_token({"sub": current_user.email, "role": current_user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 