from app.application.ports.project_repository import ProjectRepository
from app.infrastructure.db.models.project import Project
from app.infrastructure.db.models.project_member import ProjectMember

class SqlAlchemyProjectRepository(ProjectRepository):

    def __init__(self, db):
        self.db = db

    def create(self, project: Project):
        """
        Creates a project
        """
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_projects_for_user(self, user_id: int):
        """
        Returns all projects where the user is either
        creator (manager) or member.
        """
        # projects where the user is manager
        created_projects = (
            self.db.query(Project)
            .filter(Project.created_by == user_id)
        )

        # projects where the user is member
        member_projects = (
            self.db.query(Project)
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .filter(ProjectMember.user_id == user_id)
        )

        # union to avoid duplicated projects
        return created_projects.union(member_projects).all()

    def get_by_id(self, project_id: int):
        """
        Obtains a project by its ID
        """
        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    def delete(self, project: Project):
        """
        Deletes a project
        """
        self.db.delete(project)
        self.db.commit()

    def is_manager(self, project_id: int, user_id: int) -> bool:
        project = (
            self.db.query(Project)
            .filter(Project.id == project_id, Project.created_by == user_id)
            .first()
        )
        return project is not None


    def is_member(self, project_id: int, user_id: int) -> bool:
        return (
            self.db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
            .first()
            is not None
        )
