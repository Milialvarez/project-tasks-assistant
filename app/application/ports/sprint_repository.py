from abc import ABC, abstractmethod


class SprintRepository(ABC):
    @abstractmethod
    def create(self, sprint):
        pass

    @abstractmethod
    def get_by_id(self, sprint_id: int):
        pass