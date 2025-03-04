from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from services.annotation_service import AnnotationService
from models import User
from core.auth import get_current_user

router = APIRouter()

@router.post("/documents/{document_id}/annotate")
async def create_annotation(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate AI annotation for a document"""
    try:
        service = AnnotationService(db)
        result = await service.generate_annotation(document_id, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/annotations/{annotation_id}/verify")
async def verify_annotation(
    annotation_id: str,
    is_approved: bool,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Verify an annotation"""
    try:
        service = AnnotationService(db)
        result = await service.verify_annotation(annotation_id, current_user.id, is_approved)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}/annotations")
async def get_annotations(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all annotations for a document"""
    try:
        service = AnnotationService(db)
        annotations = await service.get_document_annotations(document_id)
        return annotations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 