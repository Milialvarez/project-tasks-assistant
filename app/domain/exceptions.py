# app/domain/exceptions.py

class DomainError(Exception):
    """Base exception for domain/application errors"""
    pass


class NotProjectMemberError(DomainError):
    def __init__(self):
        super().__init__("You are not a member of this project")


class NotProjectManagerError(DomainError):
    def __init__(self):
        super().__init__("You are not a manager of this project")


class ResourceNotFoundError(DomainError):
    def __init__(self, resource: str):
        super().__init__(f"{resource} with the provided ID does not exist")


class InvalidStatusError(DomainError):
    pass


class InvalidOperationError(DomainError):
    pass


# persistence
class PersistenceError(Exception):
    """Base error for persistence layer"""
    pass


class EntityAlreadyExistsError(PersistenceError):
    pass


class EntityNotFoundPersistenceError(PersistenceError):
    pass


class DatabaseUnavailableError(PersistenceError):
    pass
