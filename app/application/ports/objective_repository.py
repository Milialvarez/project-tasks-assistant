from abc import ABC, abstractmethod
from typing import List

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

    @abstractmethod
    def get(self, project_id: int | None, sprint_id: int | None)->List[Objective]:
        pass