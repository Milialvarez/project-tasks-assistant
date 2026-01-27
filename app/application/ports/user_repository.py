from abc import ABC, abstractmethod

from app.domain.entities.user import User
class UserRepository(ABC):

    @abstractmethod
    def exists(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def activate_user(self, user_id: int) -> None:
        pass
    
    @abstractmethod 
    def get_by_id(self, user_id: int):
        pass