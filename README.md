# Drone Navigation System

A full-stack drone path navigation system with a FastAPI backend for pathfinding algorithms and a React/Three.js frontend for 3D visualization.

## Project Structure

```
drone-system/
├── backend/          # FastAPI server for pathfinding algorithms
│   ├── main.py       # FastAPI application and routes
│   ├── algorithms.py # Pathfinding algorithms implementation
│   ├── models.py     # Pydantic data models
│   ├── requirements.txt
│   └── test_api.py   # API tests
└── frontend/         # React + Vite + Three.js
    ├── src/          # React components and pages
    ├── package.json
    └── vite.config.ts
```

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Python** (v3.8 or higher) - [Download](https://www.python.org/)
- **pip** (comes with Python)

### Verify Installation

```bash
# Check Node.js and npm
node --version
npm --version

# Check Python and pip
python3 --version
pip3 --version
```

## Setup Instructions

### 1. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

#### Create Virtual Environment

Create a Python virtual environment to isolate dependencies:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
.venv\Scripts\activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

#### Install Dependencies

Once the virtual environment is activated (you should see `(.venv)` in your terminal prompt):

```bash
pip3 install -r requirements.txt
```

**Dependencies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation

**Note:** Always ensure the virtual environment is activated before running the backend or installing packages.

### 2. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

## Running the Project Locally

You'll need to run both the backend and frontend servers simultaneously. Open two terminal windows or tabs.

### Terminal 1: Start the Backend Server

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
# .venv\Scripts\activate

# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1

# Start the FastAPI server
python3 -m uvicorn main:app --reload --port 8000
```

The FastAPI backend will start on `http://localhost:8000`

**Useful backend endpoints:**
- `POST http://localhost:8000/pathfind` - Calculate drone path
- `GET http://localhost:8000/docs` - Interactive API documentation (Swagger UI)
- `GET http://localhost:8000/redoc` - Alternative API documentation

### Terminal 2: Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173` (or another available port if 5173 is in use)

### Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

You should now see the drone navigation interface with the 3D visualization.

## Development Commands

### Backend

First, activate the virtual environment (from the backend directory):

```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
# .venv\Scripts\activate

# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

Then run any of these commands:

```bash
# Run with auto-reload (for development)
python3 -m uvicorn main:app --reload --port 8000

# Run tests
python3 test_api.py

# Run without auto-reload (for production)
python3 -m uvicorn main:app --port 8000

# Deactivate virtual environment (when done)
deactivate
```

### Frontend
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Common Issues & Troubleshooting

### Issue: Port Already in Use

**Backend (Port 8000 already in use):**
```bash
# Use a different port
python3 -m uvicorn main:app --reload --port 8001
```

**Frontend (Port 5173 already in use):**
```bash
# Vite will automatically use the next available port
npm run dev
```

### Issue: Module Not Found (Python)

If you get `ModuleNotFoundError`, ensure dependencies are installed:
```bash
cd backend
pip install -r requirements.txt
```

### Issue: npm Command Not Found

If npm is not recognized, reinstall Node.js from [nodejs.org](https://nodejs.org/)

### Issue: Python Command Not Found

Make sure Python is installed and added to PATH:
```bash
python3 --version
```

If `python3` is not found, try:
- macOS/Linux: `which python3`
- Windows: `where python`

### Issue: CORS Errors in Browser Console

The backend is configured to allow all origins. If you still see CORS errors:
1. Check that the backend is running on `http://localhost:8000`
2. Restart both servers
3. Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)

## API Documentation

### Pathfind Endpoint

**Request:**
```bash
curl -X POST http://localhost:8000/pathfind \
  -H "Content-Type: application/json" \
  -d '{
    "bounds": {"x": 100, "y": 100, "z": 100},
    "start": {"x": 0, "y": 0, "z": 0},
    "goal": {"x": 100, "y": 100, "z": 100},
    "obstacles": [],
    "no_fly_zones": [],
    "algorithm": "a_star"
  }'
```

For detailed API documentation, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Technologies Used

**Backend:**
- FastAPI - Modern Python web framework
- Uvicorn - ASGI web server
- Pydantic - Data validation and parsing

**Frontend:**
- React 19 - UI framework
- TypeScript - Type safety
- Vite - Build tool and dev server
- Three.js - 3D graphics
- React Three Fiber - React renderer for Three.js
- Material-UI - Component library
- Axios - HTTP client

## Support

For issues or questions, please refer to the API documentation at `http://localhost:8000/docs` when the backend is running.
