from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.task import Task

class TaskRepository(ABC):

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def filter(
        self,
        *,
        project_id: int,
        sprint_id: Optional[int],
        assigned_user_id: Optional[int],
    ) -> List[Task]:
        pass
    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        pass

    @abstractmethod
    def get_archived(self, project_id: int, sprint_id: int | None) -> List[Task]:
        pass