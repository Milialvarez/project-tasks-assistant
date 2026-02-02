from app.application.ports.user_repository import UserRepository
from app.domain.exceptions import PersistenceError, ResourceNotFoundError
from app.infrastructure.db.repositories.activation_token_repository import ActivationTokenRepository

class ActivateUserUseCase:

    def __init__(
            self, 
            user_repo: UserRepository, 
            token_repo: ActivationTokenRepository
            ):
            self.user_repo = user_repo
            self.token_repo = token_repo

    def execute(self, token_str: str):
        token = self.token_repo.get_valid_token(token_str)

        if not token:
            raise ResourceNotFoundError("Activation token")

        try:
            self.user_repo.activate_user(token.user_id)
            self.token_repo.delete(token)
        except Exception as e:
            raise PersistenceError("Failed to activate user") from e