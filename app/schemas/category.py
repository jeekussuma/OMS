from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    category: str
    description: Optional[str]
    
class CategoryResponse(CategoryBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None