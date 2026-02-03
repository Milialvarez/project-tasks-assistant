# app/domain/ports/refresh_token_repo.py
from abc import ABC, abstractmethod
from app.infrastructure.db.models.refresh_token import RefreshToken

class RefreshTokenRepository(ABC):
    @abstractmethod
    def save(self, refresh_token: RefreshToken) -> RefreshToken:
        pass

    @abstractmethod
    def get_by_token(self, token: str) -> RefreshToken | None:
        pass
    
    @abstractmethod
    def revoke(self, token: str) -> None:
        pass

    @abstractmethod
    def delete_expired(self) -> int:
        pass