from app.application.ports.refresh_token_repository import RefreshTokenRepository

class LogoutUseCase:
    def __init__(
            self, 
            refresh_token_repository: RefreshTokenRepository
            ):
            self.refresh_token_repository = refresh_token_repository

    def execute(self, refresh_token: str):
        self.refresh_token_repository.revoke(refresh_token)