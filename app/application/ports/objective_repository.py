from abc import ABC, abstractmethod

from app.domain.entities.objective import Objective


class ObjectiveRepository(ABC):

    @abstractmethod
    def create(self, objective: Objective)->Objective:
        pass

    @abstractmethod
    def update(self, objective: Objective)->Objective:
        pass

    @abstractmethod
    def get_by_id(self, objective_id: int) -> Objective | None:
        pass