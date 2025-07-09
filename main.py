from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import users, roles, permissions, departments, tasks, categories, platform

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(roles.router, prefix=f"{settings.API_V1_STR}/roles", tags=["roles"])
app.include_router(permissions.router, prefix=f"{settings.API_V1_STR}/permissions", tags=["permissions"])
app.include_router(departments.router, prefix=f"{settings.API_V1_STR}/departments", tags=["departments"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])
app.include_router(categories.router, prefix=f"{settings.API_V1_STR}/categories", tags=["categories"])
app.include_router(platform.router, prefix=f"{settings.API_V1_STR}/platforms", tags=["platforms"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Organization Management System API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }