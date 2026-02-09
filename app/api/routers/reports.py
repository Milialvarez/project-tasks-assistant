from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.reports.generate_report import GenerateReport
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.infrastructure.db.repositories.project_member_repository import SqlAlchemyProjectMemberRepository
from app.infrastructure.db.repositories.sprint_repository import SqlAlchemySprintRepository
from app.infrastructure.services.report_service import ReportService
from app.schemas.report import SprintReportResponse
from app.infrastructure.db.models import User

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/sprint/{sprint_id}", response_model=SprintReportResponse)
async def get_sprint_report(
    sprint_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Genera un reporte completo del Sprint incluyendo métricas y análisis de IA (Groq).
    """
    use_case = GenerateReport(project_member_repository=SqlAlchemyProjectMemberRepository(db),
                              sprint_repository=SqlAlchemySprintRepository(db),
                              report_service=ReportService(db))
    return await use_case.execute(sprint_id, current_user.id)