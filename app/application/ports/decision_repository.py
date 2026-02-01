from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.decision import Decision


class DecisionRepository(ABC):

    @abstractmethod
    def create(self, decision: Decision) -> Decision:
        pass

    @abstractmethod
    def update(self, decision: Decision) -> Decision:
        pass

    @abstractmethod
    def delete(self, decision: Decision) -> None:
        pass

    @abstractmethod
    def get_by_id(self, decision_id: int) -> Optional[Decision]:
        pass

    @abstractmethod
    def get_filtered(
        self,
        project_id: Optional[int],
        task_id: Optional[int],
    ) -> List[Decision]:
        pass
