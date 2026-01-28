from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.entities.activation_token import ActivationToken
from app.infrastructure.db.models.activation_token import ActivationToken as ActivationTokenModel
from app.infrastructure.db.mappers.activation_token_mapper import to_model, to_domain


class ActivationTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, token: ActivationToken):
        model = to_model(token)
        self.db.add(model)
        self.db.commit()

    def get_valid_token(self, token_str: str) -> ActivationToken | None:
        model = (
            self.db.query(ActivationTokenModel)
            .filter(
                ActivationTokenModel.token == token_str,
                ActivationTokenModel.expires_at > datetime.utcnow()
            )
            .first()
        )
        return to_domain(model) if model else None

    def delete(self, token: ActivationToken):
        model = (
            self.db.query(ActivationTokenModel)
            .filter(ActivationTokenModel.token == token.token)
            .first()
        )
        if model:
            self.db.delete(model)
            self.db.commit()
