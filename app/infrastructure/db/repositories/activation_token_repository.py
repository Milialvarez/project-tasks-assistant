from datetime import datetime
from sqlalchemy.orm import Session
from app.domain.entities.activation_token import ActivationToken
from app.infrastructure.db.mappers.activation_token_mapper import to_model

class ActivationTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, token: ActivationToken):
        model = to_model(token)
        self.db.add(model)
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
        model = to_model(token)
        self.db.delete(model)
        self.db.commit()
