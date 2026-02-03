# app/application/use_cases/login_user.py
from app.application.ports.refresh_token_repository import RefreshTokenRepository
from app.application.ports.user_repository import UserRepository
from app.core.security.jwt import JWTService
from app.infrastructure.db.models import RefreshToken
from app.domain.exceptions import AuthenticationError, UserNotActiveError
from app.infrastructure.services.password_service import PasswordService

class LoginUserUseCase:
    def __init__(self, 
                 user_repo: UserRepository, 
                 password_service: PasswordService, 
                 jwt_service: JWTService, 
                 refresh_token_repo: RefreshTokenRepository
                 ):
                self.user_repo = user_repo
                self.password_service = password_service
                self.jwt_service = jwt_service
                self.refresh_token_repo = refresh_token_repo

    def execute(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
    
        if not user or not self.password_service.verify(password, user.password_hash):
            raise AuthenticationError("Invalid email or password") 
            
        if not user.active:
            raise UserNotActiveError("Account is disabled")

        # 1. Crear Access Token
        access_token = self.jwt_service.create_access_token(str(user.id))
        
        # 2. Crear Refresh Token y Guardarlo en DB
        rt_token, rt_expire = self.jwt_service.create_refresh_token(str(user.id))
        
        refresh_token_entry = RefreshToken(
            user_id=user.id,
            token=rt_token,
            expires_at=rt_expire,
            revoked=False
        )
        self.refresh_token_repo.save(refresh_token_entry)

        return {
            "access_token": access_token,
            "refresh_token": rt_token, 
            "token_type": "bearer",
        }