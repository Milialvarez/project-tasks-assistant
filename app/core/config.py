from dotenv import load_dotenv
import os

load_dotenv()

# configure basic settings from .env
class Settings:
    PROJECT_NAME: str = "Project & Tasks Assistant"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
