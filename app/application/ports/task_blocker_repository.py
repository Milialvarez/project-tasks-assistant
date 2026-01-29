from abc import ABC, abstractmethod

from app.domain.entities.task_blocker import TaskBlocker

class BlockerRepository(ABC):
    @abstractmethod
    def create(self, comment: TaskBlocker) -> TaskBlocker:
        pass