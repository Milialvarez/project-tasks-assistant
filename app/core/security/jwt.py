# app/core/security/jwt.py
from datetime import datetime, timedelta, timezone
from jose import jwt

class JWTService:
    def __init__(self, secret, algorithm, expire_minutes):
        self.secret = secret
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, subject: str):
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)

        payload = {
            "sub": subject,
            "exp": expire
        }

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
