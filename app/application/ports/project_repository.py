from abc import ABC, abstractmethod

class ProjectRepository(ABC):

    @abstractmethod
    def create(self, project):
        pass
