from abc import ABC, abstractmethod
from typing import List

class ProjectRepository(ABC):

    @abstractmethod
    def create(self, project):
        pass
    
    @abstractmethod
    def get_projects_for_user(self, user_id: int) -> List:
        pass

    @abstractmethod
    def get_by_id(self, project_id: int):
        pass

    @abstractmethod
    def delete(self, project):
        pass

    @abstractmethod
    def is_manager(self, project_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def is_member(self, project_id: int, user_id: int) -> bool:
        pass
