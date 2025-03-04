import os
import sys
from pathlib import Path
import importlib

def check_environment():
    required_files = [
        '.env',
        'main.py',
        'models.py',
        'database.py',
        'alembic.ini',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:", missing_files)
        return False
    
    print("✅ All required files present")
    return True

def check_database():
    try:
        from database import get_db
        print("✅ Database configuration loaded")
        return True
    except Exception as e:
        print("❌ Database configuration error:", str(e))
        return False

def check_models():
    try:
        from models import Base, Project, Document, Annotation
        print("✅ Models loaded successfully")
        return True
    except Exception as e:
        print("❌ Models error:", str(e))
        return False

def main():
    print("🔍 Checking TagFlow setup...")
    
    checks = [
        check_environment(),
        check_database(),
        check_models()
    ]
    
    if all(checks):
        print("\n✨ Setup looks good! You can now run:")
        print("1. alembic upgrade head")
        print("2. uvicorn main:app --reload --port 8001")
    else:
        print("\n❌ Please fix the above errors before continuing")
        sys.exit(1)

if __name__ == "__main__":
    main() 