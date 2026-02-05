# app/application/schemas/analysis.py
from pydantic import BaseModel

class ProjectAnalysisRequest(BaseModel):
    question: str

class ProjectAnalysisResponse(BaseModel):
    answer: str
    sql_used: str | None = None 