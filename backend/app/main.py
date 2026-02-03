"""
main.py - FastAPI Application Entry Point

Purpose:
- Initializes the FastAPI application
- Configures CORS for frontend communication
- Sets up basic health check endpoint
- Loads environment variables for API keys
- Production-ready configuration

Features:
- Health check endpoint: GET /
- CORS properly configured for development and production
- Environment-aware configuration
- Uvicorn-ready for deployment
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import route modules
from app.routes.transcript_routes import router as transcript_router

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Smart Video Learning Tool API",
    description="AI-powered educational video processing API",
    version="0.1.0"
)

# ============================================
# CORS Configuration - Environment-Aware
# ============================================

# Get environment and frontend URL from .env
APP_ENV = os.getenv("APP_ENV", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Define CORS origins based on environment
if APP_ENV == "production":
    # Production: Only allow specific frontend URL
    ORIGINS = [
        FRONTEND_URL,
        "https://" + FRONTEND_URL.replace("https://", ""),  # Handle variant
    ]
    print(f"✓ Production CORS: Allowing {FRONTEND_URL}")
else:
    # Development: Allow multiple localhost variants
    ORIGINS = [
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Common React port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        FRONTEND_URL,
    ]
    print(f"✓ Development CORS: Allowing localhost variants")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    """
    Health check endpoint
    
    Returns:
    - status: String indicating the API is running
    - environment: Current deployment environment
    - version: API version
    """
    return {
        "status": "Backend running successfully",
        "environment": APP_ENV,
        "version": "0.1.0",
        "message": "Smart Video Learning Tool API is active"
    }


@app.get("/health")
async def health():
    """
    Alternative health check endpoint
    
    Used by deployment platforms (Render, Railway) for health checks
    """
    return {
        "status": "healthy",
        "environment": APP_ENV
    }


# Routes will be imported here once implemented
# Include transcript extraction routes
# Prefix "/api" makes the endpoint: POST /api/transcript/extract
app.include_router(transcript_router, prefix="/api")

# Routes available in next phases:
# from app.routes import summary_routes, quiz_routes
# app.include_router(summary_routes.router, prefix="/api")
# app.include_router(quiz_routes.router, prefix="/api")

# TODO:
# - Add summary generation routes (Phase 4)
# - Add quiz generation routes (Phase 5)
# - Setup error handling middleware
# - Add request logging for monitoring
# - Add rate limiting for production


if __name__ == "__main__":
    import uvicorn
    
    # Development mode: auto-reload enabled
    if APP_ENV == "development":
        uvicorn.run(
            app,
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            reload=True,
            log_level="info"
        )
    else:
        # Production mode: no auto-reload
        uvicorn.run(
            app,
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            reload=False,
            log_level="warning"
        )
