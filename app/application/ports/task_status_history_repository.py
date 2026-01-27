from abc import ABC, abstractmethod

from app.domain.entities.task_status_history import TaskStatusHistory


class TaskStatusHistoryRepository(ABC):

    @abstractmethod
    def create(self, history: TaskStatusHistory) -> TaskStatusHistory:
        pass

    @abstractmethod
    def get_by_task_id(self, task_id: int) -> list[TaskStatusHistory]:
        pass