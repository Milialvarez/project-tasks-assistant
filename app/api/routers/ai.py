from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.application.ai.analyze_project import AnalyzeProjectUseCase
from app.core.database import get_db, engine
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.repositories.project_member_repository import SqlAlchemyProjectMemberRepository
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.services.ai_analysis_service import LangChainAnalysisAdapter
from app.schemas.analysis import ProjectAnalysisRequest, ProjectAnalysisResponse 

router = APIRouter(prefix="/ai", tags=["AI Analysis"])

@router.post("/{project_id}/ask", response_model=ProjectAnalysisResponse)
def ask_project_intelligence(
    project_id: int, 
    request: ProjectAnalysisRequest,
    current_user_id = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Endpoint para preguntar a la IA sobre el estado del proyecto.
    Ejemplos:
    - "¿Qué tareas están bloqueadas y por qué?"
    - "¿Quién es el usuario con más tareas completadas?"
    - "¿Cuántos story points quemamos en el último sprint?"
    """
    use_case = AnalyzeProjectUseCase(ai_service = LangChainAnalysisAdapter(db_engine=engine),
                                    project_repo = SqlAlchemyProjectRepository(db),
                                    project_member_repo=SqlAlchemyProjectMemberRepository(db))

    answer_text = use_case.execute(
        project_id=project_id, 
        user_id=current_user_id, 
        question=request.question
    )
    
    return ProjectAnalysisResponse(answer=answer_text)