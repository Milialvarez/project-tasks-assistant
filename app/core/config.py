from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Project & Tasks Assistant"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
