from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None

class DepartmentInDB(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DepartmentResponse(DepartmentInDB):
    pass

class DepartmentHierarchy(DepartmentInDB):
    sub_departments: List['DepartmentHierarchy'] = []

    class Config:
        from_attributes = True

# Update forward references
DepartmentHierarchy.model_rebuild() 