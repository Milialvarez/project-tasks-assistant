import uuid
from datetime import datetime, timedelta

from app.application.ports.user_repository import UserRepository
from app.infrastructure.db.models.activation_token import ActivationToken
from app.infrastructure.db.models.user import User
from app.infrastructure.db.repositories.activation_token_repository import ActivationTokenRepository
from app.infrastructure.services.email_service import EmailService
from app.infrastructure.services.password_service import hash_password


class RegisterUserUseCase:

    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: ActivationTokenRepository,
        email_service: EmailService,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.email_service = email_service

    def execute(self, *, email: str, password: str, name: str) -> None:

        if self.user_repo.get_by_email(email):
            raise ValueError("Email already registered")

        password_hash = hash_password(password)

        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            active=False,
        )

        user = self.user_repo.create(user)

        token_str = str(uuid.uuid4())

        token = ActivationToken(
            user_id=user.id,
            token=token_str,
            expires_at=datetime.utcnow() + timedelta(hours=24),
        )

        self.token_repo.create(token)

        self.email_service.send_activation_email(
            to_email=user.email,
            token=token_str,
        )
