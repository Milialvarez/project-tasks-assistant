from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class SprintMetrics(BaseModel):
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    blocked_tasks: int
    pending_tasks: int
    completion_percentage: float

class BlockerSummary(BaseModel):
    task_title: str
    blocker_description: str

class DecisionSummary(BaseModel):
    title: str
    context: str
    impact: str
    created_at: date
    chosen_by: int

class SprintReportResponse(BaseModel):
    sprint_id: int
    sprint_name: str
    period_start: date
    period_end: date
    metrics: SprintMetrics
    active_blockers: List[BlockerSummary]
    decisions_made: List[DecisionSummary]
    ai_analysis: str 