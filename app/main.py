from fastapi import FastAPI

from app.api.routers import projects, users

app = FastAPI(
    title="Project & Tasks Assistant API",
    description="Backend for project and task management",
    version="0.1.0",
)

app.include_router(projects.router)
app.include_router(users.router)

@app.get("/")
def health_check():
    return {"status": "ok"}

