from fastapi import FastAPI, HTTPException, Depends, Body, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai
from database import get_db
from models import User, Project, Document, Annotation
from sqlalchemy import select
from datetime import datetime
import uvicorn
from typing import List
from api.v1.api import api_router
from routers import auth, documents, annotations
from middleware.error_handler import ErrorHandler
from core.config import settings
from core.logging import setup_logging, logger
from core.middleware import error_handler

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handling middleware
@app.middleware("http")
async def middleware(request: Request, call_next):
    return await error_handler(request, call_next)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix="/auth")
app.include_router(documents.router)
app.include_router(annotations.router)

class DocumentRequest(BaseModel):
    text: str
    project_id: str

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up TagFlow API")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down TagFlow API")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "status": "online",
        "app": "TagFlow",
        "time": datetime.utcnow().isoformat()
    }

@app.post("/api/annotate")
async def annotate_document(
    request: DocumentRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        # verify project exists
        project = await db.execute(
            select(Project).where(Project.id == request.project_id)
        )
        project = project.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # create document
        document = Document(
            project_id=request.project_id,
            content=request.text
        )
        db.add(document)
        await db.flush()

        # get annotations from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes text and provides annotations."},
                {"role": "user", "content": f"Please analyze this text and provide key annotations: {request.text}"}
            ]
        )
        
        annotations = response.choices[0].message.content.split('\n')
        
        # store annotation in db
        annotation = Annotation(
            document_id=document.id,
            content=annotations,
            model_version="gpt-3.5-turbo"
        )
        db.add(annotation)
        await db.flush()

        return {"annotations": annotations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects")
async def create_project(
    project_data: dict = Body(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        # create default schema if none provided
        default_schema = {
            "type": "text_classification",
            "labels": ["positive", "negative", "neutral"],
            "multi_label": False
        }
        
        new_project = Project(
            name=project_data['name'],
            description=project_data.get('description', ''),
            schema=project_data.get('schema', default_schema),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        
        return {
            "id": str(new_project.id),
            "name": new_project.name,
            "description": new_project.description,
            "schema": new_project.schema,
            "created_at": new_project.created_at.isoformat()
        }
    except Exception as e:
        print(f"Project creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects")
async def get_projects(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Project))
        projects = result.scalars().all()
        return [
            {
                "id": str(p.id),
                "name": p.name,
                "schema": p.schema,
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat()
            }
            for p in projects
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
def get_config():
    return {"db_url": os.getenv("DATABASE_URL")}

@app.get("/api/projects/{project_id}/documents")
async def get_project_documents(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document).where(Document.project_id == project_id)
    )
    documents = result.scalars().all()
    return [{
        "id": doc.id,
        "content": doc.content,
        "metadata": {
            "status": "annotated" if doc.annotations else "pending"
        }
    } for doc in documents]

@app.get("/api/documents/{document_id}/annotations")
async def get_document_annotations(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Annotation).where(Annotation.document_id == document_id)
    )
    annotations = result.scalars().all()
    return [{"id": ann.id, "content": ann.content} for ann in annotations]

@app.put("/api/documents/{document_id}")
async def update_document(
    document_id: str,
    content: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    document.content = content
    await db.commit()
    return {"message": "Document updated successfully"}

@app.get("/api/projects/{project_id}/stats")
async def get_project_stats(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    # add project statistics logic
    pass

@app.get("/test")
async def test():
    return {
        "status": "ok",
        "message": "TagFlow API is working!",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/projects/{project_id}/documents/batch")
async def upload_documents(
    project_id: str,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        uploaded_docs = []
        for file in files:
            content = await file.read()
            doc = Document(
                project_id=project_id,
                content=content.decode(),
                status="pending"
            )
            db.add(doc)
            uploaded_docs.append(doc)
        
        await db.commit()
        return {"message": f"Successfully uploaded {len(uploaded_docs)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/{document_id}/annotate")
async def annotate_document(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        # get document
        doc = await db.get(Document, document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # get project schema
        project = await db.get(Project, doc.project_id)
        
        # generate AI annotation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an expert at {project.schema['type']} annotation. Available labels: {project.schema['labels']}"},
                {"role": "user", "content": f"Please analyze this text and provide labels: {doc.content}"}
            ],
            temperature=0.3
        )
        
        # calculate confidence score (example)
        confidence_score = 0.85  # maybe implement more sophisticated scoring later 
        
        # create annotation
        annotation = Annotation(
            document_id=document_id,
            content=response.choices[0].message.content,
            confidence_score=confidence_score,
            verified=False
        )
        
        db.add(annotation)
        await db.commit()
        
        return {
            "annotation": annotation.content,
            "confidence_score": confidence_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
