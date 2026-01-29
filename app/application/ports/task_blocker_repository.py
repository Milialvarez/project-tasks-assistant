from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.task_blocker import TaskBlocker
from app.domain.enums import BlockerStatus

class BlockerRepository(ABC):
    @abstractmethod
    def create(self, comment: TaskBlocker) -> TaskBlocker:
        pass

    @abstractmethod
    def get_by_task_id(self, *, task_id: int, status: BlockerStatus | None = None) -> List[TaskBlocker]:
        pass

    @abstractmethod
    def get_by_id(self, blocker_id:int) -> TaskBlocker | None:
        pass

    @abstractmethod
    def update(self, blocker: TaskBlocker) -> TaskBlocker:
        pass