from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.auth.logout_use_case import LogoutUseCase
from app.application.auth.refresh_token_use_case import RefreshTokenUseCase
from app.core.database import get_db
from app.core.security.jwt import JWTService
from app.application.auth.login_user import LoginUserUseCase
from app.infrastructure.db.repositories.refresh_token_repository import SqlAlchemyRefreshTokenRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.infrastructure.services.password_service import PasswordService
from app.schemas.auth import LoginRequest, RefreshTokenRequest, TokenResponse
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])
def get_jwt_service():
    return JWTService(
        secret=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_expire_days=getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7)
    )

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    
    use_case = LoginUserUseCase(
        user_repo=SqlAlchemyUserRepository(db),
        password_service=PasswordService(),
        jwt_service=get_jwt_service(),
        refresh_token_repo=SqlAlchemyRefreshTokenRepository(db) 
    )

    try:
        return use_case.execute(email=data.email, password=data.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    
    use_case = RefreshTokenUseCase(
        refresh_token_repo=SqlAlchemyRefreshTokenRepository(db),
        jwt_service=get_jwt_service(),
        user_repo=SqlAlchemyUserRepository(db)
    )
    
    try:
        result = use_case.execute(refresh_token=data.refresh_token)
        return {
            "access_token": result["access_token"],
            "refresh_token": data.refresh_token, 
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    use_case = LogoutUseCase(refresh_token_repo=SqlAlchemyRefreshTokenRepository(db))
    
    use_case.execute(refresh_token=data.refresh_token)
    return {"message": "Logout succesfully from your account"}