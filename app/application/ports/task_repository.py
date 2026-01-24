from abc import ABC, abstractmethod
from app.infrastructure.db.models.task import Task

class TaskRepository(ABC):

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def filter(
        self,
        *,
        project_id: int | None,
        sprint_id: int | None,
        assigned_user_id: int | None,
    ) -> list[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, task: Task) -> None:
        pass