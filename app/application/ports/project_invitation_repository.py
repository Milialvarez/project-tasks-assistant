from abc import ABC, abstractmethod
from app.domain.entities.project_invitation import ProjectInvitation

class ProjectInvitationRepository(ABC):

    @abstractmethod
    def create(self, invitation: ProjectInvitation) -> ProjectInvitation:
        pass

    @abstractmethod
    def get_pending(self, project_id: int, user_id: int):
        pass

    @abstractmethod
    def get_by_id(self, invitation_id: int):
        pass

    @abstractmethod
    def update(self, invitation: ProjectInvitation):
        pass
