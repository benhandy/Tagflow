from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, UUID, Enum, Float, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid
import enum
import axios, { AxiosInstance } from 'axios'

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    ANNOTATOR = "annotator"
    VIEWER = "viewer"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.ANNOTATOR)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    hashed_password = Column(String, nullable=False)
    
    # Add relationships
    projects = relationship("Project", back_populates="creator")
    annotations = relationship("Annotation", back_populates="created_by_user")
    verified_annotations = relationship("Annotation", back_populates="verified_by_user")

class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    schema = Column(JSON, nullable=False)  # Annotation schema configuration
    created_by = Column(UUID, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Add relationships
    creator = relationship("User", back_populates="projects")
    documents = relationship("Document", back_populates="project")

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID, ForeignKey('projects.id'))
    content = Column(String, nullable=False)
    status = Column(String, default='pending')  # pending, annotated, verified
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Add relationships
    project = relationship("Project", back_populates="documents")
    annotations = relationship("Annotation", back_populates="document")

class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID, ForeignKey('documents.id'))
    created_by = Column(UUID, ForeignKey('users.id'))
    content = Column(JSON, nullable=False)
    confidence_score = Column(Float)
    verified = Column(Boolean, default=False)
    verified_by = Column(UUID, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Add relationships
    document = relationship("Document", back_populates="annotations")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="annotations")
    verified_by_user = relationship("User", foreign_keys=[verified_by], back_populates="verified_annotations")

export class ApiClient:
    private api: AxiosInstance
    
    constructor() {
        this.api = axios.create({
            baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
            headers: {
                'Content-Type': 'application/json',
            },
        })

        # Add token to requests if it exists
        this.api.interceptors.request.use((config) => {
            const token = localStorage.getItem('token')
            if (token) {
                config.headers.Authorization = `Bearer ${token}`
            }
            return config
        })
    }

    # Auth endpoints
    async login(email: string, password: string) {
        const response = await this.api.post('/token', {
            username: email,  # OAuth2 expects username
            password,
        })
        const { access_token } = response.data
        localStorage.setItem('token', access_token)
        return response.data
    }

    async signup(userData: {
        email: string;
        password: string;
        name: string;
        role?: string;
    }) {
        const response = await this.api.post('/signup', userData)
        const { access_token } = response.data
        localStorage.setItem('token', access_token)
        return response.data
    }

    # Project endpoints
    async getProjects() {
        const response = await this.api.get('/api/projects')
        return response.data
    }

    async createProject(projectData: {
        name: string;
        description?: string;
        schema: any;
    }) {
        const response = await this.api.post('/api/projects', projectData)
        return response.data
    }

    # Document endpoints
    async getProjectDocuments(projectId: string) {
        const response = await this.api.get(`/api/projects/${projectId}/documents`)
        return response.data
    }

    async uploadDocument(projectId: string, content: string) {
        const response = await this.api.post(`/api/projects/${projectId}/documents`, {
            content,
        })
        return response.data
    }

    # Annotation endpoints
    async createAnnotation(documentId: string) {
        const response = await this.api.post(`/api/documents/${documentId}/annotate`)
        return response.data
    }

    async verifyAnnotation(annotationId: string, isApproved: boolean) {
        const response = await this.api.post(`/api/annotations/${annotationId}/verify`, {
            is_approved: isApproved,
        })
        return response.data
    }

    async getDocumentAnnotations(documentId: string) {
        const response = await this.api.get(`/api/documents/${documentId}/annotations`)
        return response.data
    }

# Create a singleton instance
export const apiClient = new ApiClient() 