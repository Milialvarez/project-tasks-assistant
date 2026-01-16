from abc import ABC, abstractmethod

class UserRepository(ABC):

    @abstractmethod
    def exists(self, user_id: int) -> bool:
        pass
