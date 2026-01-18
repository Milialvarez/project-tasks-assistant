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
    try:
        use_case = RegisterUserUseCase(
            SqlAlchemyUserRepository(UserRepository),
            ActivationTokenRepository(db),
            EmailService()
        )
        use_case.execute(data.email, data.password, data.name)
        return {"message": "Check your email to activate your account"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activate")
def activate_user(token: str, db: Session = Depends(get_db)):
    try:
        use_case = ActivateUserUseCase(
            UserRepository(db),
            ActivationTokenRepository(db)
        )
        use_case.execute(token)
        return {"message": "Account activated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
