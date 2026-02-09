import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime
from app.infrastructure.db.models import Sprint, Task, Project, ProjectMember, TaskBlocker
from app.domain.enums import TaskStatus, ProjectRole, SprintStatus, BlockerStatus
from app.infrastructure.services.report_service import ReportService 

@pytest.mark.asyncio
async def test_get_sprint_report_success_with_mocked_ai(async_client, db_session):
    project = Project(name="Project AI", created_by=1, created_at=datetime.now())
    db_session.add(project)
    db_session.commit()
    
    member = ProjectMember(project_id=project.id, user_id=1, role=ProjectRole.manager)
    db_session.add(member)

    sprint = Sprint(
        project_id=project.id, 
        name="Sprint 1", 
        status=SprintStatus.active,
        started_at=datetime.now(),
        ended_at=None
    )
    db_session.add(sprint)
    db_session.commit()

    task1 = Task(project_id=project.id, sprint_id=sprint.id, title="Task A", current_status=TaskStatus.completed)
    task2 = Task(project_id=project.id, sprint_id=sprint.id, title="Task B", current_status=TaskStatus.blocked)
    db_session.add_all([task1, task2])
    db_session.commit()

    blocker = TaskBlocker(
        task_id=task2.id, 
        cause="API caída", 
        created_by=1, 
        status=BlockerStatus.active,
        start_date=datetime.now(),
        solved_at=None
    )
    db_session.add(blocker)
    db_session.commit()

    mock_ai_text = "### Resumen Mockeado\nTodo va excelente."

    with patch.object(ReportService, "_generate_ai_analysis", new_callable=AsyncMock) as mock_method:
        mock_method.return_value = mock_ai_text

        response = await async_client.get(f"/reports/sprint/{sprint.id}")

    assert response.status_code == 200
    json_data = response.json()

    assert json_data["sprint_name"] == "Sprint 1"
    assert json_data["metrics"]["completion_percentage"] == 50.0
    assert json_data["ai_analysis"] == mock_ai_text 