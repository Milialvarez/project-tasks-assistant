from app.application.ports.refresh_token_repository import RefreshTokenRepository
import logging

logger = logging.getLogger(__name__)

class CleanupTokensUseCase:
    def __init__(self, refresh_token_repo: RefreshTokenRepository):
        self.refresh_token_repo = refresh_token_repo

    def execute(self):
        count = self.refresh_token_repo.delete_expired()
        if count > 0:
            logger.info(f"Cleanup job: Deleted {count} expired refresh tokens.")