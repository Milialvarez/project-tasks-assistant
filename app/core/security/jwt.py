from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional

class JWTService:
    def __init__(self, secret, algorithm, expire_minutes, refresh_expire_days=7):
        self.secret = secret
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
        self.refresh_expire_days = refresh_expire_days 

    def create_access_token(self, subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        payload = {"sub": subject, "exp": expire, "type": "access"}
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_refresh_token(self, subject: str) -> tuple[str, datetime]:
        # Retorna el token string y la fecha de expiración para guardarla en DB
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_expire_days)
        payload = {"sub": subject, "exp": expire, "type": "refresh"}
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return token, expire

    def decode_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except JWTError:
            return None