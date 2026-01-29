from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.sprint import Sprint
class SprintRepository(ABC):
    @abstractmethod
    def create(self, sprint: Sprint):
        pass

    @abstractmethod
    def get_by_id(self, sprint_id: int):
        pass

    @abstractmethod
    def update(self, sprint: Sprint):
        pass

    @abstractmethod
    def get_sprints_by_project_id(self, project_id: int)-> List[Sprint]:
        pass