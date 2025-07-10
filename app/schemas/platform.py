from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PlatformBase(BaseModel):
    platform: str
    
class PlatformResponse(PlatformBase):
    id: str
