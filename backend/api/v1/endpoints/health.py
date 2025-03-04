from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from services.cache import CacheService

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Check system health"""
    checks = {
        "database": True,
        "cache": True,
        "ai_service": True
    }
    
    try:
        # Check database
        await db.execute("SELECT 1")
    except Exception:
        checks["database"] = False
    
    try:
        # Check cache
        cache = CacheService()
        await cache.set("health_check", "ok")
    except Exception:
        checks["cache"] = False
        
    return {
        "status": "healthy" if all(checks.values()) else "unhealthy",
        "checks": checks
    } 