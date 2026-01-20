from datetime import datetime
from sqlalchemy.orm import Session

from app.infrastructure.db.models.activation_token import ActivationToken


class ActivationTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, token: ActivationToken):
        self.db.add(token)
        self.db.commit()

    def get_valid_token(self, token_str: str) -> ActivationToken | None:
        return (
            self.db.query(ActivationToken)
            .filter(
                ActivationToken.token == token_str,
                ActivationToken.expires_at > datetime.utcnow()
            )
            .first()
        )

    def delete(self, token: ActivationToken):
        self.db.delete(token)
        self.db.commit()
