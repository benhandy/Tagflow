from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Annotation, Document, User, Project
from typing import List, Optional
from schemas.annotation import AnnotationCreate, AnnotationResponse, BatchAnnotationResponse
from auth.roles import require_admin, require_annotator, require_viewer
import openai
from services.ai_annotation_service import AIAnnotationService, AIAnnotationError

router = APIRouter(prefix="/api/annotations", tags=["annotations"])

@router.post("/{document_id}", response_model=AnnotationResponse)
async def create_annotation(
    document_id: str,
    annotation: AnnotationCreate,
    current_user: User = Depends(require_annotator),  # Only admins and annotators can create
    db: AsyncSession = Depends(get_db)
):
    # Verify document exists
    document = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = document.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Create annotation
    db_annotation = Annotation(
        document_id=document_id,
        content=annotation.content,
        confidence_score=annotation.confidence_score,
        created_by=current_user.id
    )
    db.add(db_annotation)
    await db.commit()
    await db.refresh(db_annotation)
    return db_annotation

@router.put("/{annotation_id}/verify", response_model=AnnotationResponse)
async def verify_annotation(
    annotation_id: str,
    current_user: User = Depends(require_admin),  # Only admins can verify
    db: AsyncSession = Depends(get_db)
):
    annotation = await db.execute(
        select(Annotation).where(Annotation.id == annotation_id)
    )
    annotation = annotation.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")

    annotation.verified = True
    annotation.verified_by = current_user.id
    await db.commit()
    await db.refresh(annotation)
    return annotation

@router.get("/document/{document_id}", response_model=List[AnnotationResponse])
async def get_document_annotations(
    document_id: str,
    current_user: User = Depends(require_viewer),  # All authenticated users can view
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Annotation).where(Annotation.document_id == document_id)
    )
    annotations = result.scalars().all()
    return annotations

@router.post("/batch/{project_id}", response_model=BatchAnnotationResponse)
async def batch_annotate_documents(
    project_id: str,
    document_ids: List[str],
    model: str = "gpt-3.5-turbo",
    background_tasks: BackgroundTasks = None,
    current_user = Depends(require_annotator),
    db: AsyncSession = Depends(get_db)
):
    """Batch annotate multiple documents with enhanced AI"""
    try:
        # Get project and documents
        project = await db.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        documents = []
        for doc_id in document_ids:
            doc = await db.get(Document, doc_id)
            if doc and doc.project_id == project_id:
                documents.append(doc)

        if not documents:
            raise HTTPException(status_code=404, detail="No valid documents found")

        # Initialize AI service
        ai_service = AIAnnotationService(model)
        
        # Process annotations
        stored_annotations = []
        for doc in documents:
            try:
                result = await ai_service.annotate_document(doc, project, db)
                
                db_annotation = Annotation(
                    document_id=doc.id,
                    content=result,
                    model_version=model,
                    confidence_score=result.get('confidence', 0),
                    created_by=current_user.id,
                    needs_review=result.get('needs_review', False)
                )
                db.add(db_annotation)
                stored_annotations.append(db_annotation)
                
            except AIAnnotationError as e:
                # Log error but continue with other documents
                print(f"Error annotating document {doc.id}: {str(e)}")
                continue
        
        await db.commit()
        
        return {
            "message": f"Successfully annotated {len(stored_annotations)} documents",
            "annotations": stored_annotations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{annotation_id}/correct")
async def correct_annotation(
    annotation_id: str,
    corrections: dict,
    current_user = Depends(require_annotator),
    db: AsyncSession = Depends(get_db)
):
    """Submit corrections and update AI model"""
    annotation = await db.get(Annotation, annotation_id)
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")

    # Update the annotation with corrections
    annotation.content = corrections
    annotation.verified = True
    annotation.verified_by = current_user.id
    
    # Feed correction back to AI for learning
    ai_service = AIAnnotationService()
    await ai_service.learn_from_corrections(db, annotation.document_id, corrections)
    
    await db.commit()
    return {"message": "Annotation corrected and AI model updated"} 