from sqlalchemy.orm import Session
from app.infrastructure.ai.ollama_client import OllamaClient
from app.infrastructure.services.task_analitycs_service import TaskAnalyticsService


class ExplainProjectDelaysUseCase:
    def __init__(self, db: Session):
        self.analytics_service = TaskAnalyticsService(db)
        self.ai_client = OllamaClient()

    def execute(self, project_id: int, sprint_id: int | None = None) -> dict:
        summary = self.analytics_service.get_project_delay_summary(
            project_id=project_id,
            sprint_id=sprint_id,
        )

        explanation = self.ai_client.explain_delays(summary)

        return {
            "analytics": summary,
            "ai_explanation": explanation,
        }
