from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, UUID, Enum, Float, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid
import enum

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
    
    projects = relationship("Project", back_populates="creator")
    annotations = relationship("Annotation", back_populates="created_by_user")
    verified_annotations = relationship("Annotation", back_populates="verified_by_user")

class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    schema = Column(JSON, nullable=False)
    created_by = Column(UUID, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = relationship("User", back_populates="projects")
    documents = relationship("Document", back_populates="project")

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID, ForeignKey('projects.id'))
    content = Column(String, nullable=False)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
    
    document = relationship("Document", back_populates="annotations")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="annotations")
    verified_by_user = relationship("User", foreign_keys=[verified_by], back_populates="verified_annotations") 