from app.application.ports.ai_analysis_service import AIAnalysisService
from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.project_repository import ProjectRepository 
from app.domain.exceptions import ResourceNotFoundError, NotProjectMemberError

class AnalyzeProjectUseCase:
    def __init__(self, 
                 ai_service: AIAnalysisService, 
                 project_repo: ProjectRepository,
                 project_member_repo: ProjectMemberRepository):
                self.ai_service = ai_service
                self.project_repo = project_repo
                self.project_member_repo = project_member_repo

    def execute(self, project_id: int, user_id: int, question: str) -> str:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ResourceNotFoundError("Project not found")

        if not self.project_member_repo.is_member(project_id, user_id):
            raise NotProjectMemberError("User relies not belong to this project")

        answer = self.ai_service.analyze_project(project_id, question)
        
        return answer