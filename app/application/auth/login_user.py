from app.domain.exceptions import AuthenticationError, UserNotActiveError

class LoginUserUseCase:
    def __init__(self, user_repo, password_service, jwt_service):
        self.user_repo = user_repo
        self.password_service = password_service
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise AuthenticationError("Invalid credentials")

        if not user.active:
            raise UserNotActiveError("User not activated")

        if not self.password_service.verify(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        return {
            "access_token": self.jwt_service.create_access_token(str(user.id)),
            "token_type": "bearer",
        }
