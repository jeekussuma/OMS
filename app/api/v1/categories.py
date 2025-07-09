from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryResponse
from datetime import timedelta
from app.core.config import settings
from app.core.dependencies import get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    roles = db.query(Category).offset(skip).limit(limit).all()
    return roles