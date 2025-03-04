from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Project, Document, User
from typing import List
from schemas.project import ProjectCreate, ProjectResponse
from auth.roles import UserRole, require_admin, require_annotator, require_viewer

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    current_user: User = Depends(require_viewer),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate, 
    current_user: User = Depends(require_admin),  # Only admins can create projects
    db: AsyncSession = Depends(get_db)
):
    db_project = Project(**project.dict(), created_by=current_user.id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(require_viewer),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_update: ProjectCreate,
    current_user: User = Depends(require_annotator),  # Admins and annotators can update
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Additional check: only admins or project creators can update
    if current_user.role != UserRole.ADMIN.value and project.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this project")
    
    for key, value in project_update.dict().items():
        setattr(project, key, value)
    
    await db.commit()
    await db.refresh(project)
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: User = Depends(require_admin),  # Only admins can delete
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.delete(project)
    await db.commit()
    return {"message": "Project deleted successfully"} 