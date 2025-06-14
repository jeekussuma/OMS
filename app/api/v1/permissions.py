from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.role import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse

router = APIRouter()

@router.post("/", response_model=PermissionResponse)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.name == permission.name).first()
    if db_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission name already exists"
        )
    
    db_permission = Permission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.get("/", response_model=List[PermissionResponse])
def read_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    permissions = db.query(Permission).offset(skip).limit(limit).all()
    return permissions

@router.get("/{permission_id}", response_model=PermissionResponse)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return db_permission

@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(permission_id: int, permission: PermissionUpdate, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    
    update_data = permission.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_permission, field, value)
    
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    
    db.delete(db_permission)
    db.commit()
    return None 