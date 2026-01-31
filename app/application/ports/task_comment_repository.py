from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.task_comment import TaskComment


class CommentRepository(ABC):
    @abstractmethod
    def create(self, comment: TaskComment) -> TaskComment:
        pass

    @abstractmethod
    def get_comments(self, task_id: int)->List[TaskComment]:
        pass

    @abstractmethod
    def get_by_id(self, comment_id: int)->TaskComment | None:
        pass

    @abstractmethod
    def update(self, comment:TaskComment)->TaskComment:
        pass

    @abstractmethod
    def delete(self, comment_id: int)-> None:
        pass