from pydantic import BaseModel, EmailStr

class ProjectInvitationCreate(BaseModel):
    invited_email: EmailStr