from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.models.platform import Platform
from app.models.user import User
from app.schemas.platform import PlatformResponse
from datetime import timedelta
from app.core.config import settings
from app.core.dependencies import get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError

router = APIRouter()

@router.get("/", response_model=List[PlatformResponse])
def read_platforms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    roles = db.query(Platform).offset(skip).limit(limit).all()
    return roles

@router.get("/{platform_id}", response_model=PlatformResponse)
def read_platform(
    platform_id: str,
    db: Session = Depends(get_db),
):
    db_platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if db_platform is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )
    return db_platform