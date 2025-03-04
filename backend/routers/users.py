from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import User

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.query(User).all()
    return users 