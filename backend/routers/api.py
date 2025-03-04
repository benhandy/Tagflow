from fastapi import APIRouter
from . import users, projects, documents, annotations

api_router = APIRouter(prefix="/api")

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(annotations.router, prefix="/annotations", tags=["annotations"]) 