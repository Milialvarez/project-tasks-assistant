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