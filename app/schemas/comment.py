from datetime import datetime
from pydantic import BaseModel

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    content: str
    created_at: datetime
    edited_at: datetime | None
    
    class Config:
        from_attributes = True  
