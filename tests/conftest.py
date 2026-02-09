import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.dependencies.auth import get_current_user, get_current_user_id
from app.main import app 
from app.infrastructure.db.base import Base 
from app.infrastructure.db.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    user = User(
        email="test@test.com", 
        password_hash="fakehash", 
        name="Test User", 
        active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    user_test = db_session.query(User).filter_by(email="test@test.com").first()

    def _get_current_user_override():
        return user_test
    
    def _get_current_user_id_override():
        return user_test.id

    app.dependency_overrides[get_db] = _get_db_override
    app.dependency_overrides[get_current_user] = _get_current_user_override
    app.dependency_overrides[get_current_user_id] = _get_current_user_id_override

    return app 

@pytest_asyncio.fixture(scope="function")
async def async_client(client):
    transport = ASGITransport(app=client)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()