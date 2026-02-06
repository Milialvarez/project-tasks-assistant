from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.projects.accept_invitation import AcceptProjectInvitationUseCase
from app.application.projects.delete_project import DeleteProjectUseCase
from app.application.projects.delete_project_member import DeleteProjectMember
from app.application.projects.get_user_projects import GetUserProjectsUseCase
from app.application.projects.invite_member import InviteProjectMemberUseCase
from app.application.projects.reject_invitation import RejectProjectInvitationUseCase
from app.application.projects.update_project import UpdateProjectUseCase
from app.core.database import get_db
from app.application.projects.create_project import CreateProjectUseCase
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.repositories.project_invitation_repository import SqlAlchemyProjectInvitationRepository
from app.infrastructure.db.repositories.project_member_repository import SqlAlchemyProjectMemberRepository
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.infrastructure.services.email_service import EmailService
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.project_invitation import ProjectInvitationCreate

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Creates a project
    
    :param name: represents the name of the project
    :type name: str
    :param description: represents the description of the project
    :type description: str | None
    :param db: db session available to execute the operation
    :type db: Session
    """
    use_case = CreateProjectUseCase(
        project_repository=SqlAlchemyProjectRepository(db),
        project_member_repository=SqlAlchemyProjectMemberRepository(db),
        user_repository=SqlAlchemyUserRepository(db),
    )

    return use_case.execute(
            project=project,
            created_by=current_user_id,
        )


@router.get("/me", response_model=List[ProjectResponse],
    status_code=200)
def get_user_projects(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Get all the projects of a user
    
    :param user_id: id of the user
    :type user_id: int
    :param db: db session available to execute the operation
    :type db: Session
    """

    use_case = GetUserProjectsUseCase(
        project_repository=SqlAlchemyProjectRepository(db),
        user_repository=SqlAlchemyUserRepository(db),
    )

    return use_case.execute(current_user_id)

@router.put("/{project_id}", response_model=ProjectResponse, status_code=201)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Update a project
    
    :param project_id: id of the project that will be updated
    :type project_id: int
    :param name: optional name to replace the original
    :type name: str | None
    :param description: optional description to replace the original
    :type description: str | None
    :param db: db session available to execute the operation
    :type db: Session
    """
    use_case = UpdateProjectUseCase(
        project_repository=SqlAlchemyProjectRepository(db)
    )

    return use_case.execute(
            project_id=project_id,
            project_data=project,
            user_id=current_user_id,
        )


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """
    Delete a project
    
    :param project_id: id of the project that will be deleted
    :type project_id: int
    :param db: db session available to execute the operation
    :type db: Session
    """

    use_case = DeleteProjectUseCase(
        project_repository=SqlAlchemyProjectRepository(db))

    use_case.execute(
            project_id=project_id,
            user_id=current_user_id
        )

    return {"message": "Project deleted successfully"}

@router.post("/{project_id}/invite", status_code=201)
def invite_project_member(
    project_id: int,
    data: ProjectInvitationCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    use_case = InviteProjectMemberUseCase(
        project_repository=SqlAlchemyProjectRepository(db),
        user_repository=SqlAlchemyUserRepository(db),
        invitation_repository=SqlAlchemyProjectInvitationRepository(db),
        member_repository=SqlAlchemyProjectMemberRepository(db),
        email_service=EmailService(),
    )

    invitation = use_case.execute(
        project_id=project_id,
        invited_email=data.invited_email,
        current_user_id=current_user_id,
    )

    return {
        "message": "Invitation sent successfully",
        "invitation_id": invitation.id,
    }


@router.post("/invitations/{invitation_id}/accept")
def accept_project_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    use_case = AcceptProjectInvitationUseCase(
        invitation_repository=SqlAlchemyProjectInvitationRepository(db),
        member_repository=SqlAlchemyProjectMemberRepository(db),
    )

    use_case.execute(invitation_id=invitation_id, user_id=current_user_id)
    return {"message": "Invitation accepted"}

@router.post("/invitations/{invitation_id}/reject")
def reject_project_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    use_case = RejectProjectInvitationUseCase(
        invitation_repository=SqlAlchemyProjectInvitationRepository(db)
    )

    use_case.execute(
            invitation_id=invitation_id,
            user_id=current_user_id,
        )
    return {"message": "Invitation rejected"}

@router.delete("/{project_id}/member/{user_id}")
def delete_project_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
    ):
    use_case=DeleteProjectMember(
        project_repository=SqlAlchemyProjectRepository(db),
        project_member_repository=SqlAlchemyProjectMemberRepository(db))
    
    use_case.execute(
        project_id,
        user_id,
        current_user_id
    )

    return {"message": "Project Member successfully deleted"}