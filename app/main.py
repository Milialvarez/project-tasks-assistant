from fastapi import FastAPI

app = FastAPI(
    title="Project & Tasks Assistant API",
    description="Backend for project and task management",
    version="0.1.0",
)

@app.get("/")
def health_check():
    return {"status": "ok"}
