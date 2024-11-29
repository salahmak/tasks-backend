from fastapi import FastAPI
from app.routes import task_routes

# Create database tables
# Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Task Management API server")


# Include routers
app.include_router(task_routes.router, prefix="/api/v1", tags=["tasks"])


# Optional health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
