from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
import logging
from fastapi import HTTPException
from core.config import settings

load_dotenv()

# build the DATABASE_URL from settings
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

if DATABASE_URL is None:
    raise ValueError("Database URL is not configured. Check your .env file.")

# create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# create async session
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# dependency to get DB session
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 
