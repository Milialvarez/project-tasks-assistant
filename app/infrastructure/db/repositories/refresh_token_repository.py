# app/infrastructure/repositories/sqlalchemy_refresh_token_repo.py
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.application.ports.refresh_token_repository import RefreshTokenRepository
from app.infrastructure.db.models import RefreshToken

class SqlAlchemyRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_by_token(self, token: str) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def revoke(self, token: str) -> None:
        # Buscamos y actualizamos
        rt = self.get_by_token(token)
        if rt:
            rt.revoked = True
            self.db.commit()

    def delete_expired(self) -> int:
        now = datetime.now(timezone.utc)
        # SQLAlchemy permite borrar directo con el query
        deleted_count = self.db.query(RefreshToken).filter(
            RefreshToken.expires_at < now
        ).delete()
        
        self.db.commit()
        return deleted_count