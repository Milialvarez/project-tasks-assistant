from app.application.ports.project_member_repository import ProjectMemberRepository
from app.application.ports.sprint_repository import SprintRepository
from app.domain.exceptions import NotProjectMemberError, ResourceNotFoundError
from app.infrastructure.services.report_service import ReportService


class GenerateReport:
    def __init__(
            self,
            *,
            project_member_repository: ProjectMemberRepository,
            sprint_repository: SprintRepository,
            report_service: ReportService
    ):
        self.project_member_repository= project_member_repository
        self.sprint_repository= sprint_repository
        self.report_service=report_service

    async def execute(self, sprint_id: int, current_user_id: int):
        sprint = self.sprint_repository.get_by_id(sprint_id)
        if not sprint:
            raise ResourceNotFoundError("Sprint")
        
        if not self.project_member_repository.is_member(sprint.project_id, current_user_id):
            raise NotProjectMemberError()
        
        return await self.report_service.generate_sprint_report(sprint_id)