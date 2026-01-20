# app/application/auth/login_user.py
class LoginUserUseCase:
    def __init__(self, user_repo, password_service, jwt_service):
        self.user_repo = user_repo
        self.password_service = password_service
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")

        if not user.active:
            raise ValueError("User not activated")

        if not self.password_service.verify(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        access_token = self.jwt_service.create_access_token(
            subject=str(user.id)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
