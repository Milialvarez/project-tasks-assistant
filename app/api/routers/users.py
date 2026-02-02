from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.application.ports.user_repository import UserRepository
from app.application.users.activate_user import ActivateUserUseCase
from app.application.users.register_user import RegisterUserUseCase
from app.core.database import get_db
from app.infrastructure.db.repositories.activation_token_repository import ActivationTokenRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.infrastructure.services.email_service import EmailService
from app.schemas.user import RegisterUserRequest

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(data: RegisterUserRequest, db: Session = Depends(get_db)):
    use_case = RegisterUserUseCase(
        SqlAlchemyUserRepository(db),
        ActivationTokenRepository(db),
        EmailService()
    )

    use_case.execute(
        email=data.email,
        password=data.password,
        name=data.name,
    )

    return {"message": "Check your email to activate your account"}


@router.get("/activate")
def activate_user(token: str, db: Session = Depends(get_db)):
    use_case = ActivateUserUseCase(
        SqlAlchemyUserRepository(db),
        ActivationTokenRepository(db)
    )

    use_case.execute(token)

    return {"message": "Account activated successfully"}
