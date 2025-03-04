from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Document, Project, User
from typing import List
from schemas.document import DocumentCreate, DocumentResponse
from auth.roles import require_admin, require_annotator, require_viewer

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.post("/{project_id}/upload", response_model=List[DocumentResponse])
async def upload_documents(
    project_id: str,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(require_annotator),  # Only admins and annotators can upload
    db: AsyncSession = Depends(get_db)
):
    # Verify project exists and user has access
    project = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = project.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Only project creator or admin can upload documents
    if current_user.role != "ADMIN" and project.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to upload to this project")

    uploaded_docs = []
    for file in files:
        content = await file.read()
        doc = Document(
            project_id=project_id,
            content=content.decode(),
            status="pending",
            created_by=current_user.id
        )
        db.add(doc)
        uploaded_docs.append(doc)
    
    await db.commit()
    return uploaded_docs

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(require_viewer),  # All authenticated users can view
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(require_admin),  # Only admins can delete
    db: AsyncSession = Depends(get_db)
):
    document = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = document.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    await db.delete(document)
    await db.commit()
    return {"message": "Document deleted successfully"} 