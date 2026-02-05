# app/application/schemas/analysis.py
from typing import Optional
from pydantic import BaseModel

class ProjectAnalysisRequest(BaseModel):
    question: str

class ProjectAnalysisResponse(BaseModel):
    answer: str
    sql_used: Optional[str] = None