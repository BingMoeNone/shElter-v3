# Quickstart Guide: Wiki Platform

## Prerequisites

- Node.js 18+ with npm/yarn
- Python 3.11+
- PostgreSQL 15+
- Docker and Docker Compose (optional but recommended)
- Git

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd wiki-platform
```

### 2. Backend Setup

#### Using Virtual Environment (Recommended)

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

#### Database Setup

```bash
# Create database and run migrations
alembic upgrade head
```

#### Run Backend Server

```bash
# Activate virtual environment first
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install

# Copy environment variables
cp .env.example .env
# Edit .env with your configuration

# Run development server
npm run dev
```

### 4. Using Docker (Alternative)

```bash
# From project root
docker-compose up --build
```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost/wiki_platform
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000
```

## API Endpoints

The API is served at `http://localhost:8000/api/v1`

### Available Endpoints

- `POST /auth/login` - User authentication
- `POST /users` - Register new user
- `GET /articles` - List articles
- `POST /articles` - Create new article
- `GET /search?q=query` - Search articles

## Development Scripts

### Backend

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Format code
black src tests

# Lint code
flake8 src tests
```

### Frontend

```bash
# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Lint code
npm run lint

# Format code
npm run format
```

## Project Structure

```
backend/
鈹溾攢鈹€ src/
鈹?  鈹溾攢鈹€ models/          # Pydantic models
鈹?  鈹溾攢鈹€ schemas/         # API schemas
鈹?  鈹溾攢鈹€ services/        # Business logic
鈹?  鈹溾攢鈹€ api/             # API routes
鈹?  鈹溾攢鈹€ database/        # DB configuration
鈹?  鈹斺攢鈹€ main.py          # Application entry point
鈹溾攢鈹€ tests/               # Test files
鈹斺攢鈹€ requirements.txt     # Python dependencies

frontend/
鈹溾攢鈹€ src/
鈹?  鈹溾攢鈹€ components/      # Vue components
鈹?  鈹溾攢鈹€ views/           # Page components
鈹?  鈹溾攢鈹€ composables/     # Vue composition functions
鈹?  鈹溾攢鈹€ services/        # API service wrappers
鈹?  鈹斺攢鈹€ stores/          # Pinia stores
鈹溾攢鈹€ tests/               # Test files
鈹斺攢鈹€ package.json         # Node.js dependencies
```

## Common Tasks

### Creating a New API Endpoint

1. Define the route in `backend/src/api/`
2. Create corresponding Pydantic models in `backend/src/schemas/`
3. Implement business logic in `backend/src/services/`
4. Add tests in `backend/tests/`

### Adding a New Component

1. Create component in `frontend/src/components/`
2. Add tests in `frontend/tests/unit/`
3. Import and use in parent components

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## Upgrade Interfaces

The system includes several upgrade interfaces to facilitate future technology migrations:

1. **Database Layer**: Abstracted with SQLAlchemy interfaces
2. **Authentication**: Pluggable auth module
3. **Search**: Search interface allowing swap between PostgreSQL FTS and Elasticsearch
4. **File Storage**: Abstraction layer for local/cloud storage
5. **Real-time Communication**: WebSocket interface abstraction

## Troubleshooting

### Backend Issues

- If getting database connection errors, ensure PostgreSQL is running and credentials are correct
- For dependency issues, try recreating the virtual environment

### Frontend Issues

- If getting API connection errors, verify backend server is running on port 8000
- For build issues, try clearing node_modules and reinstalling dependencies

### Docker Issues

- Ensure Docker has sufficient resources allocated
- Check logs with `docker-compose logs -f`