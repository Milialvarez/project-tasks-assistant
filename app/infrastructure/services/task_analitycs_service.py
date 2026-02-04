from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.infrastructure.db.models.task import Task
from app.infrastructure.db.models.task_status_history import TaskStatusHistory
from app.infrastructure.db.models.task_blocker import TaskBlocker
from app.domain.enums import TaskStatus


class TaskAnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_project_delay_summary(
        self,
        project_id: int,
        sprint_id: int | None = None,
    ) -> dict:
        query = self.db.query(Task).filter(
            Task.project_id == project_id,
            Task.archived.is_(False),
        )

        if sprint_id:
            query = query.filter(Task.sprint_id == sprint_id)

        tasks = query.all()

        total_tasks = len(tasks)

        blocked_tasks_data = []
        long_running_tasks = []

        for task in tasks:
            # --- BLOCKERS ---
            blockers = (
                self.db.query(TaskBlocker)
                .filter(
                    TaskBlocker.task_id == task.id,
                    TaskBlocker.solved_at.is_(None),
                )
                .all()
            )

            for blocker in blockers:
                days_blocked = (datetime.utcnow() - blocker.start_date).days
                blocked_tasks_data.append({
                    "task_id": task.id,
                    "cause": blocker.cause,
                    "days_blocked": days_blocked,
                })

            # --- STATUS HISTORY ---
            history_count = (
                self.db.query(TaskStatusHistory)
                .filter(TaskStatusHistory.task_id == task.id)
                .count()
            )

            if task.current_status != TaskStatus.COMPLETED:
                days_in_progress = (datetime.utcnow() - task.created_at).days
                if days_in_progress >= 3 or history_count >= 4:
                    long_running_tasks.append({
                        "task_id": task.id,
                        "days_in_progress": days_in_progress,
                        "status_changes": history_count,
                        "current_status": task.current_status.value,
                    })

        return {
            "project_id": project_id,
            "sprint_id": sprint_id,
            "total_tasks": total_tasks,
            "blocked_tasks": blocked_tasks_data,
            "long_running_tasks": long_running_tasks,
        }
