from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.infrastructure.db.models import *  # noqa
