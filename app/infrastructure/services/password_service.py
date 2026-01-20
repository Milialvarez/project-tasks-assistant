from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


class PasswordService:
    def hash(self, password: str) -> str:
        return hash_password(password)

    def verify(self, password: str, hashed: str) -> bool:
        return verify_password(password, hashed)
