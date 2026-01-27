from app.domain.entities.activation_token import ActivationToken
from app.infrastructure.db.models.activation_token import ActivationToken as ActivationTokenModel

def to_domain(model: ActivationTokenModel) -> ActivationToken:
    return ActivationToken(
        id=model.id,
        user_id=model.user_id,
        token=model.token,
        expires_at=model.expires_at,
    )

def to_model(entity: ActivationToken) -> ActivationTokenModel:
    return ActivationTokenModel(
        id=entity.id,
        user_id=entity.user_id,
        token=entity.token,
        expires_at=entity.expires_at,
    )
