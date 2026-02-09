import pytest
from sqlalchemy import select
from app.infrastructure.db.models import Project, ProjectMember
from app.domain.enums import ProjectRole

@pytest.mark.asyncio
async def test_create_project_success(async_client, db_session):
    payload = {
        "name": "Proyecto Alpha",
        "description": "Un proyecto de prueba super genial"
    }

    response = await async_client.post("/projects/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Proyecto Alpha"
    assert "id" in data

    project_in_db = db_session.scalar(select(Project).where(Project.name == "Proyecto Alpha"))
    assert project_in_db is not None
    
    member_in_db = db_session.scalar(
        select(ProjectMember).where(ProjectMember.project_id == project_in_db.id)
    )
    assert member_in_db is not None
    assert member_in_db.user_id == 1 
    assert member_in_db.role == ProjectRole.manager

@pytest.mark.asyncio
async def test_create_project_empty_name_fails(async_client):
    payload = {
        "name": "   ", 
        "description": "Esto debería fallar"
    }
    
    with pytest.raises(ValueError) as excinfo:
        await async_client.post("/projects/", json=payload)
    
    assert str(excinfo.value) == "Project name cannot be empty"
