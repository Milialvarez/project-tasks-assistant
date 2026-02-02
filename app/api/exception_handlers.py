from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

from app.domain.exceptions import (
    AuthenticationError,
    DomainError,
    NotProjectMemberError,
    NotProjectManagerError,
    ResourceNotFoundError,
    InvalidStatusError,
    InvalidOperationError,
    PersistenceError,
    UserNotActiveError,
)

def domain_error_handler(_: Request, exc: DomainError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


def not_member_handler(_: Request, exc: NotProjectMemberError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )


def not_manager_handler(_: Request, exc: NotProjectManagerError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )


def not_found_handler(_: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

def persistence_error_handler(_: Request, exc: PersistenceError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

def auth_error_handler(_: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


def not_active_handler(_: Request, exc: UserNotActiveError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )