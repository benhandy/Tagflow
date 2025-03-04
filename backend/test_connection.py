import requests
import sys

def test_backend_connection():
    try:
        response = requests.get("http://localhost:8001/test")
        print("✅ Backend is running!")
        print("Response:", response.json())
        return True
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend!")
        print("Make sure you're running: uvicorn main:app --reload --host 0.0.0.0 --port 8001")
        return False

if __name__ == "__main__":
    print("Testing backend connection...")
    if not test_backend_connection():
        sys.exit(1) 