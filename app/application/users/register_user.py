import uuid
from datetime import datetime, timedelta

from app.application.ports.user_repository import UserRepository
from app.domain.entities.activation_token import ActivationToken
from app.domain.entities.user import User
from app.infrastructure.db.repositories.activation_token_repository import ActivationTokenRepository
from app.infrastructure.services.email_service import EmailService
from app.infrastructure.services.password_service import hash_password
from app.domain.exceptions import EntityAlreadyExistsError, PersistenceError

class RegisterUserUseCase:
    def __init__(
            self, 
            user_repo: UserRepository, 
            token_repo: ActivationTokenRepository, 
            email_service: EmailService
            ):
            self.user_repo = user_repo
            self.token_repo = token_repo
            self.email_service = email_service

    def execute(self, *, email: str, password: str, name: str):

        if self.user_repo.get_by_email(email):
            raise EntityAlreadyExistsError("Email already registered")

        user = self.user_repo.create(
            User(
                email=email,
                password_hash=hash_password(password),
                name=name,
                active=False,
                created_at=datetime.now(),
            )
        )

        token = ActivationToken(
            user_id=user.id,
            token=str(uuid.uuid4()),
            expires_at=datetime.utcnow() + timedelta(hours=24),
        )

        try:
            self.token_repo.create(token)
        except Exception as e:
            raise PersistenceError("Failed to create activation token") from e

        self.email_service.send_activation_email(
            to_email=user.email,
            token=token.token,
        )

