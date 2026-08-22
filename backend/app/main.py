from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import reports, analytics
# Import our database configuration and models
from .database import engine, Base
from .routers import reports


# 1. Create database tables automatically
# (If the tables already exist, this safely does nothing)
Base.metadata.create_all(bind=engine)

# 2. Initialize the FastAPI application
app = FastAPI(
    title="Ocean Hazard AI-GIS API",
    description="Backend for crowdsourced ocean hazard reporting and social media analytics.",
    version="1.0.0"
)

# 3. Configure CORS (Cross-Origin Resource Sharing)
# This allows your frontend application to communicate with this backend.
origins = [
    "http://localhost",
    "http://localhost:3000",   # Default React port
    "http://127.0.0.1:5500",   # Default VS Code Live Server port
    "http://localhost:5173",   # Default Vite port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)

# 4. Include the routers
app.include_router(reports.router)

# 5. Root endpoint / Health Check
@app.get("/", tags=["Health"])
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Ocean Hazard AI-GIS API",
        "docs": "Visit /docs for the interactive API documentation."
    }
app.include_router(reports.router)
app.include_router(analytics.router)