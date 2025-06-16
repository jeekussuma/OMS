from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentHierarchy
from datetime import datetime
from app.core.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # If parent_id is provided, verify it exists
    if department.parent_id:
        parent = db.query(Department).filter(Department.id == department.parent_id).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent department with id {department.parent_id} not found"
            )
    
    # Check if department name already exists in the same parent
    existing_dept = db.query(Department).filter(
        Department.name == department.name,
        Department.parent_id == department.parent_id
    ).first()
    
    if existing_dept:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department with this name already exists in the same parent"
        )
    
    # Create new department
    db_department = Department(
        name=department.name,
        description=department.description,
        parent_id=department.parent_id
    )
    
    try:
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[DepartmentResponse])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Department)
    
    if parent_id is not None:
        query = query.filter(Department.parent_id == parent_id)
    else:
        # If no parent_id specified, return only root departments
        query = query.filter(Department.parent_id.is_(None))
    
    departments = query.offset(skip).limit(limit).all()
    return [
        DepartmentResponse(
            id=dept.id,
            name=dept.name,
            description=dept.description,
            parent_id=dept.parent_id,
            created_at=dept.created_at or datetime.utcnow(),
            updated_at=dept.updated_at
        ) for dept in departments
    ]

@router.get("/hierarchy", response_model=List[DepartmentHierarchy])
def get_department_hierarchy(db: Session = Depends(get_db)):
    """Get the complete department hierarchy"""
    def build_hierarchy(dept):
        return DepartmentHierarchy(
            id=dept.id,
            name=dept.name,
            description=dept.description,
            parent_id=dept.parent_id,
            created_at=dept.created_at or datetime.utcnow(),
            updated_at=dept.updated_at,
            sub_departments=[build_hierarchy(sub) for sub in dept.sub_departments]
        )
    
    # Get all root departments (those without parents)
    root_departments = db.query(Department).filter(Department.parent_id.is_(None)).all()
    return [build_hierarchy(dept) for dept in root_departments]

@router.get("/{department_id}", response_model=DepartmentResponse)
def read_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return DepartmentResponse(
        id=db_department.id,
        name=db_department.name,
        description=db_department.description,
        parent_id=db_department.parent_id,
        created_at=db_department.created_at or datetime.utcnow(),
        updated_at=db_department.updated_at
    )

@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # If parent_id is being updated, verify it exists and check for circular reference
    if department.parent_id is not None:
        if department.parent_id == department_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department cannot be its own parent"
            )
        
        parent = db.query(Department).filter(Department.id == department.parent_id).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent department with id {department.parent_id} not found"
            )
        
        # Check if the new parent is not a descendant of this department
        current = parent
        while current.parent_id is not None:
            if current.parent_id == department_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot set a descendant department as parent"
                )
            current = current.parent
    
    # Check for name uniqueness in the same parent
    if department.name is not None:
        existing_dept = db.query(Department).filter(
            Department.name == department.name,
            Department.parent_id == (department.parent_id or db_department.parent_id),
            Department.id != department_id
        ).first()
        
        if existing_dept:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department with this name already exists in the same parent"
            )
    
    update_data = department.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_department, field, value)
    
    db.commit()
    db.refresh(db_department)
    return DepartmentResponse(
        id=db_department.id,
        name=db_department.name,
        description=db_department.description,
        parent_id=db_department.parent_id,
        created_at=db_department.created_at or datetime.utcnow(),
        updated_at=db_department.updated_at
    )

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # Check if department has sub-departments
    sub_departments = db.query(Department).filter(Department.parent_id == department_id).first()
    if sub_departments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete department with sub-departments"
        )
    
    # Check if department has users
    if db_department.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete department with assigned users"
        )
    
    db.delete(db_department)
    db.commit()
    return None 