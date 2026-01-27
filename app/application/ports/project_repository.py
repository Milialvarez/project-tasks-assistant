from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.project import Project

class ProjectRepository(ABC):

    @abstractmethod
    def create(self, project: Project) -> Project:
        pass

    @abstractmethod
    def update(self, project: Project) -> Project:
        pass

    @abstractmethod
    def get_projects_for_user(self, user_id: int) -> List[Project]:
        pass

    @abstractmethod
    def get_by_id(self, project_id: int) -> Project | None:
        pass

    @abstractmethod
    def delete(self, project: Project):
        pass

    @abstractmethod
    def is_manager(self, project_id: int, user_id: int) -> bool:
        pass
