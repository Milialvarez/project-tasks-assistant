from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.exception_handlers import (
    authentication_exception_handler, domain_error_handler, 
    not_active_handler, not_found_handler, 
    not_manager_handler, not_member_handler, persistence_error_handler
)
from app.api.routers import auth, decisions, objective, projects, sprints, tasks, users
from app.domain.exceptions import (
    AuthenticationError, DomainError, NotProjectManagerError, 
    NotProjectMemberError, PersistenceError, ResourceNotFoundError, 
    TokenExpiredError, TokenRevokedError, UserNotActiveError
)

from app.infrastructure.services.scheduler import start_scheduler, scheduler 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- 🟢 LIFESPAN STARTUP ---")
    start_scheduler()
    
    yield  
    
    print("--- 🔴 LIFESPAN SHUTDOWN ---") 
    scheduler.shutdown()


app = FastAPI(
    title="Project & Tasks Assistant API",
    description="Backend for project and task management",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(projects.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sprints.router)
app.include_router(tasks.router)
app.include_router(objective.router)
app.include_router(decisions.router)

app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(NotProjectMemberError, not_member_handler)
app.add_exception_handler(NotProjectManagerError, not_manager_handler)
app.add_exception_handler(ResourceNotFoundError, not_found_handler)
app.add_exception_handler(PersistenceError, persistence_error_handler)
app.add_exception_handler(AuthenticationError, authentication_exception_handler)
app.add_exception_handler(UserNotActiveError, not_active_handler)
app.add_exception_handler(TokenExpiredError, authentication_exception_handler)
app.add_exception_handler(TokenRevokedError, authentication_exception_handler)


@app.get("/")
def health_check():
    return {"status": "ok"}

