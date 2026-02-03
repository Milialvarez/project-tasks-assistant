# app/application/use_cases/refresh_token.py
from datetime import datetime, timezone
from app.application.ports.refresh_token_repository import RefreshTokenRepository
from app.application.ports.user_repository import UserRepository
from app.core.security.jwt import JWTService
from app.domain.exceptions import AuthenticationError, ResourceNotFoundError, TokenExpiredError, TokenRevokedError, UserNotActiveError

class RefreshTokenUseCase:
    def __init__(
            self, 
            refresh_token_repo: RefreshTokenRepository, 
            jwt_service: JWTService, 
            user_repo: UserRepository
            ):
            self.refresh_token_repo = refresh_token_repo
            self.jwt_service = jwt_service
            self.user_repo = user_repo

    def execute(self, refresh_token: str):
        payload = self.jwt_service.decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationError("Invalid token signature or type")

        stored_token = self.refresh_token_repo.get_by_token(refresh_token)
        if not stored_token:
            raise ResourceNotFoundError("Token not found")
            
        if stored_token.revoked:
            raise TokenRevokedError("Token has been revoked")

        expires_at = stored_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if expires_at < datetime.now(timezone.utc):
             raise TokenExpiredError("Refresh token expired")

        user_id = payload.get("sub")
        user = self.user_repo.get_by_id(user_id)
        if not user:
             raise ResourceNotFoundError(f"User with id {user_id} not found")
        
        if not user.active:
             raise UserNotActiveError("User is inactive")

        new_access_token = self.jwt_service.create_access_token(str(user.id))
        
        return {
            "access_token": new_access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }