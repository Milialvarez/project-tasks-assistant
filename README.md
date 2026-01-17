# Project & Tasks Assistant API

Backend API for managing projects, tasks, and team collaboration, built with **FastAPI** and designed following **Hexagonal Architecture (Ports & Adapters)** principles.
This project focuses on clean architecture, separation of concerns, and scalability, making it suitable for real-world backend applications.

---

## Project Overview

**Project & Tasks Assistant** is an API that allows users to:

- Create and manage projects
- Organize tasks within projects
- Track task status and history
- Collaborate with multiple users per project
- Manage decisions, objectives, sprints, and blockers

The main goal of this project is to practice and apply **clean backend architecture**, business rules isolation, and testable code.

---

## Architecture

The project follows **Hexagonal Architecture**, separating the system into clear layers:
app/
├── api/ # HTTP layer (FastAPI routers)
├── application/ # Use cases (business workflows)
├── domain/ # Business rules, entities, enums
├── infrastructure/ # Database models, repositories, adapters
├── core/ # App configuration & database setup
└── main.py # Application entrypoint


### Why Hexagonal Architecture?

- Business logic is independent of frameworks
- Easy to test use cases without HTTP or database
- Infrastructure can change without affecting domain logic
- Clear responsibility per layer

---

## Core Concepts

- **Domain**: Defines business rules and constraints (enums, validations, entities).
- **Application**: Contains use cases (e.g. *Create Project*, *Create Task*).
- **Infrastructure**: SQLAlchemy models, repositories, database access.
- **API**: FastAPI endpoints acting as adapters to the outside world.

---

## Main Features (Current & Planned)

### Projects
- Create projects
- Assign a creator to each project
- Validate project creation rules
- List projects

### Tasks
- Create tasks inside projects
- Track task status (pending, in progress, completed)
- Task comments and blockers
- Task status history

### Collaboration
- Project members
- Project invitations
- Role-based access (planned)

### Organization
- Sprints
- Objectives
- Decisions tracking

---

## Technologies Used

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy 2.0**
- **Alembic** (database migrations)
- **PostgreSQL**
- **Pydantic**
- **Uvicorn**
- **Pytest** (testing)
- **Docker** (planned)

---

## Environment Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/project-tasks-assistant.git
cd project-tasks-assistant
```
### 2. Create the virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure environment variables
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
ENVIRONMENT=development
```
### 5. Run migrations
```bash
alembic upgrade head
```
### 6. Run the application
```bash
uvicorn app.main:app --reload
```

---

## Testing
Tests are written using pytest and focus on: Use cases, business rules, API integration


## 🎯 Project Goals
- Practice clean architecture and SOLID principles
- Build a maintainable backend structure
 -Serve as a portfolio-ready backend project
- Simulate real-world backend development patterns
