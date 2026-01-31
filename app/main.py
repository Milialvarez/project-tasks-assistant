from fastapi import FastAPI

from app.api.routers import auth, objective, projects, sprints, tasks, users

app = FastAPI(
    title="Project & Tasks Assistant API",
    description="Backend for project and task management",
    version="0.1.0",
)

app.include_router(projects.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sprints.router)
app.include_router(tasks.router)
app.include_router(objective.router)

@app.get("/")
def health_check():
    return {"status": "ok"}

