from abc import ABC, abstractmethod
from app.domain.entities.project_member import ProjectMember

class ProjectMemberRepository(ABC):

    @abstractmethod
    def add_member(self, member: ProjectMember) -> ProjectMember:
        pass

    @abstractmethod
    def is_member(self, project_id: int, user_id: int) -> bool:
        pass
    
    @abstractmethod
    def delete(self, project_id: int, user_id: int):
        pass