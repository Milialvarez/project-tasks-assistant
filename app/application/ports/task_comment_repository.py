from abc import ABC, abstractmethod

from app.domain.entities.task_comment import TaskComment


class CommentRepository(ABC):
    @abstractmethod
    def create(self, comment: TaskComment) -> TaskComment:
        pass