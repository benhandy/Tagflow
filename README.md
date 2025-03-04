# Tagflow

A tool to turn raw data into production ML datasets in minutes, not months.

Tagflow is an AI-powered document annotation tool built with FastAPI and React, designed to streamline the process of creating high-quality training data for machine learning models.

## Project Structure

```
annotation_tool/
├── backend/           # FastAPI backend
│   ├── api/           # REST API endpoints and routing
│   ├── core/          # Core configurations, settings, and utilities
│   ├── models/        # Database models and schema definitions
│   └── services/      # Business logic and application services
└── front/             # React frontend application
    └── src/           # Source files for UI components and state management
```

## Setup Instructions

### Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Install required dependencies
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to the frontend directory
cd front

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

## Key Features

- **User Authentication**: Secure login and user management system
- **Project Management**: Create, organize, and manage annotation projects
- **Document Annotation**: Intuitive interface for annotating various document types
- **AI-powered Suggestions**: Leverage OpenAI GPT to accelerate annotation with smart suggestions
- **Verification Workflow**: Quality assurance process to verify annotations for accuracy

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database for persistent storage

### Frontend
- **React**: JavaScript library for building user interfaces
- **TypeScript**: Static typing for improved code quality
- **Axios**: HTTP client for API requests

### Authentication
- **JWT**: JSON Web Tokens for secure authentication

### AI Integration
- **OpenAI GPT**: Natural language processing for annotation suggestions


### Contributing
We welcome contributions! If you'd like to contribute to TagFlow, please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes.

Submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contact
For questions or feedback, please reach out to benhandy9@gmail.com.

