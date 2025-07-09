from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PlatformBase(BaseModel):
    platform: str
    
class PlatformResponse(PlatformBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None