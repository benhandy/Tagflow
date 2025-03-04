from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        # Get database URL from environment
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return False
            
        print(f"Testing connection to: {database_url}")
        
        # Create engine
        engine = create_engine(database_url)
        
        # Try to connect and execute a test query
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))  # Use text() to wrap the SQL
            first_result = result.scalar()
            print(f"✅ Connection successful! Test query returned: {first_result}")
            return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 