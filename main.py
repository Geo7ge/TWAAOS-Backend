from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes.locations_routes import router as location_router
from routes.user_routes import router as user_router
from routes.sponsors_routes import router as sponsors_router
from routes.events_routes import router as events_router 
from routes.registration_routes import router as registration_router
from routes.auth_routes import router as auth_router
from routes.feedback_routes import router as feedback_router
from routes.notification_routes import router as notifications_router
from routes.file_routes import router as files_router
from routes.event_sponsor_routes import router as event_sponsor_router

from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(location_router)
app.include_router(sponsors_router)
app.include_router(events_router)
app.include_router(registration_router)
app.include_router(auth_router)
app.include_router(feedback_router)
app.include_router(notifications_router)
app.include_router(files_router)
app.include_router(event_sponsor_router)
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
