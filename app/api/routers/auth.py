from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security.jwt import JWTService
from app.application.auth.login_user import LoginUserUseCase
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.infrastructure.services.password_service import PasswordService
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        use_case = LoginUserUseCase(
            user_repo=SqlAlchemyUserRepository(db),
            password_service=PasswordService(),
            jwt_service=JWTService(
                secret=settings.SECRET_KEY,
                algorithm=settings.ALGORITHM,
                expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            )
        )

        return use_case.execute(
            email=data.email,
            password=data.password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
