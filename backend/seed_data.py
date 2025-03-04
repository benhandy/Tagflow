import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from models import Project, Document, Annotation

async def seed_database():
    async with AsyncSessionLocal() as session:
        # Create a test project
        test_project = Project(
            name="Test Project",
            description="A project for testing the annotation system"
        )
        session.add(test_project)
        await session.flush()

        # Create a test document
        test_document = Document(
            project_id=test_project.id,
            content="This is a test document for annotation."
        )
        session.add(test_document)
        await session.flush()

        # Create a test annotation
        test_annotation = Annotation(
            document_id=test_document.id,
            content=["Test annotation 1", "Test annotation 2"],
            model_version="gpt-3.5-turbo"
        )
        session.add(test_annotation)
        
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_database()) 