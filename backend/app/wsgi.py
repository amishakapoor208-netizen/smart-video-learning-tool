"""
wsgi.py - WSGI Entry Point for Production Deployment

Purpose:
- Provides WSGI application for deployment platforms (Render, Railway, Heroku)
- Used by production ASGI servers (Gunicorn, Uvicorn)
- Separate from main.py for cleaner deployment

Usage:
- Platform deployment: gunicorn app.wsgi:app
- Or: uvicorn app.wsgi:app --host 0.0.0.0 --port 8000
"""

from app.main import app

# WSGI/ASGI application - used by deployment servers
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
