from app.application.ports.refresh_token_repository import RefreshTokenRepository

class LogoutUseCase:
    def __init__(
            self, 
            refresh_token_repo: RefreshTokenRepository
            ):
            self.refresh_token_repo = refresh_token_repo

    def execute(self, refresh_token: str):
        self.refresh_token_repo.revoke(refresh_token)