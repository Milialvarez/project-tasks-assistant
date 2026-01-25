from abc import ABC, abstractmethod


class SprintRepository(ABC):
    @abstractmethod
    def create(self, sprint):
        pass