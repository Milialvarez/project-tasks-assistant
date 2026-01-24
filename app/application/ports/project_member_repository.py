from abc import ABC, abstractmethod
from app.infrastructure.db.models.project_member import ProjectMember

class ProjectMemberRepository(ABC):

    @abstractmethod
    def add_member(self, member: ProjectMember) -> ProjectMember:
        pass
