from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no definida")

from app.infrastructure.db.base import Base
from app.infrastructure.db.models import (
    user,
    project,
    project_member,
    project_invitation,
    task,
    task_comment,
    task_blocker,
    task_status_history,
    decision,
    objective,
    sprint,
)


engine = create_engine(DATABASE_URL, echo=True)

def run():
    print("Creando esquema inicial...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente")

if __name__ == "__main__":
    run()
