from abc import ABC, abstractmethod

class TaskRepository(ABC):

    @abstractmethod
    def create(self, project):
        pass