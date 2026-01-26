from abc import ABC, abstractmethod

from app.infrastructure.db.models.sprint import Sprint


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