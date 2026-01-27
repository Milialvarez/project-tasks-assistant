from app.domain.entities.user import User
from app.infrastructure.db.models.user import User as UserModel

def to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        password_hash=model.password_hash,
        name=model.name,
        active=model.active,
        created_at=model.created_at,
    )

def to_model(entity: User) -> UserModel:
    return UserModel(
        id=entity.id,
        email=entity.email,
        password_hash=entity.password_hash,
        name=entity.name,
        active=entity.active,
    )
