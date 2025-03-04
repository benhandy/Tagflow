import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session
from models import User, Project, Document  # Import from models package
from datetime import datetime
import uuid
from utils.security import get_password_hash

async def seed_database():
    try:
        async with async_session() as session:
            # Create admin user
            admin_user = User(
                id=uuid.uuid4(),
                email="admin@tagflow.ai",
                name="Admin User",
                role="ADMIN",
                hashed_password=get_password_hash("admin123")
            )
            session.add(admin_user)
            
            # Create annotator user
            annotator = User(
                id=uuid.uuid4(),
                email="annotator@tagflow.ai",
                name="Test Annotator",
                role="ANNOTATOR",
                hashed_password=get_password_hash("annotator123")
            )
            session.add(annotator)
            await session.flush()  # Flush to get the IDs

            # Create sample project
            project = Project(
                id=uuid.uuid4(),
                name="Sample Project",
                description="A sample project for testing TagFlow",
                schema={
                    "labels": ["PERSON", "ORGANIZATION", "LOCATION"],
                    "attributes": {
                        "confidence": "float",
                        "source": "string"
                    }
                },
                created_by=admin_user.id
            )
            session.add(project)
            await session.flush()

            # Create sample document
            document = Document(
                id=uuid.uuid4(),
                project_id=project.id,
                content="John Smith works at Apple Inc. in Cupertino, California.",
                status="pending"
            )
            session.add(document)

            await session.commit()
            print("✅ Database seeded successfully!")
            
            # Print created data
            print("\nCreated Users:")
            print(f"Admin: {admin_user.email}")
            print(f"Annotator: {annotator.email}")
            print(f"\nCreated Project: {project.name}")
            print(f"Created Document ID: {document.id}")

    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        raise

def main():
    try:
        asyncio.run(seed_database())
    except KeyboardInterrupt:
        print("\nSeeding interrupted by user")
    except Exception as e:
        print(f"Failed to seed database: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 