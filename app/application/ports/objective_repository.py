from abc import ABC, abstractmethod

from app.domain.entities.objective import Objective


class ObjectiveRepository(ABC):

    @abstractmethod
    def create(self, objective: Objective)->Objective:
        pass