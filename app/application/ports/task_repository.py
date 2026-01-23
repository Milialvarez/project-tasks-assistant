from abc import ABC, abstractmethod
from app.infrastructure.db.models.task import Task

class TaskRepository(ABC):

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass
