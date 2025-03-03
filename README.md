# Tagflow
A Tool to Turn Raw Data into Production ML Datasets in Minutes, Not Months


An AI-powered document annotation tool built with FastAPI and React.

## project structure 

"""
 annotation_tool/
├── backend/ # FastAPI backend
│ ├── api/ # API endpoints
│ ├── core/ # Core configurations
│ ├── models/ # Database models
│ └── services/ # Business logic
└── front/ # React frontend
└── src/ # Source files

"""

## Setup:


### Backend

bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

### Frontend 


bash
cd front
npm install
npm run dev






## Features

- User authentication
- Project management
- Document annotation
- AI-powered annotation suggestions
- Annotation verification workflow

## Tech Stack

- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Frontend: React, TypeScript, Axios
- Authentication: JWT
- AI: OpenAI GPT
