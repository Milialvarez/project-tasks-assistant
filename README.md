# Smart Project & Tasks Assistant API

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![AI Power](https://img.shields.io/badge/AI-Powered%20by%20Groq-f55036?style=for-the-badge&logo=openai&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Hexagonal-orange?style=for-the-badge)

A high-performance backend API designed for managing agile projects, built with **Clean Architecture** principles and supercharged with **Generative AI** for real-time business intelligence.

---

## Project Overview

**Project & Tasks Assistant**  is an intelligent system designed to help agile teams organize their work while providing an **AI-driven assistant** capable of answering natural language questions about the project's state.

The system is built to demonstrate advanced backend patterns:
* **Hexagonal Architecture (Ports & Adapters):** Ensuring total decoupling between business logic and infrastructure.
* **Generative AI Integration:** Using LLMs to interpret database schemas and generate complex SQL queries on the fly (Text-to-SQL).
* **Scalability:** Ready for real-world scenarios with background tasks, email services, and secure authentication.

---

## AI & Project Intelligence 

This project integrates a cutting-edge **Text-to-SQL** engine that acts as a virtual **"Scrum Master"**. It translates human questions into database queries and interprets the results using business context strategies.

### Tech Stack for AI
* **Inference Engine:** [Groq](https://groq.com/) (LPU Inference) for ultra-low latency responses.
* **LLM Model:** **Llama 3.3 (70B Versatile)**.
* **Orchestration:** **LangChain** (SQLDatabase Chain & Prompt Templates).
* **Strategy:** RAG-like approach with minimal schema injection and business rule enforcement via prompt engineering.

### What can the AI do?
Instead of hardcoding static reports, users can ask dynamic questions to the API:

> *"Why is the current sprint delayed?"*
> (The AI checks specifically for 'active' blockers, incomplete tasks, and user workload).

> *"Who is the top performer this month?"*
> (Calculates completed tasks grouped by user and joined with project members).

**Key Differentiator:** The AI service uses a "Business Strategy Injection" to teach the LLM specific domain rules (e.g., distinguishing between a 'blocker' and a simple 'bug'), ensuring accurate, role-based answers.

---

## Architecture

The project strictly follows **Hexagonal Architecture**, separating the code into concentric layers:

```text
app/
├── api/             # Primary Adapters (FastAPI Routes, Pydantic Schemas)
├── application/     # Application Layer (Use Cases, Ports Interfaces)
├── domain/          # Enterprise Logic (Entities, Enums, Value Objects)
├── infrastructure/  # Secondary Adapters (SQLAlchemy, Groq Service, Email)
└── core/            # Configuration & Wiring
```
---

## Key Features
-  Intelligent Analysis
     Natural Language Querying: Chat with your database in plain English (or Spanish).
     Context-Aware Responses: The AI acts as a Project Manager, giving recommendations based on live data and specific business rules.
     Smart Strategies: The system injects strategies into the prompt to distinguish between simple bugs and critical blockers.

-  Project Management
     Complete CRUD for Projects.
     Role-Based actions
     Invitation System: Secure invitation flow via email tokens.

-  Agile Workflow
     Sprints: Create, start, and finish sprints.
     Tasks: Status history, user comments.
     Blockers: Track impediments linked to specific tasks (used by AI for diagnosis).
     Objectives and decisions to declare in projects, sprints and tasks.

-  Security & Background
    JWT Authentication: Secure access with Access/Refresh tokens.
    Email Service: Async email sending for account activation and invites.
    Background Tasks: Scheduler for utomatic cleanup of expired tokens.
    Reports generator: usings AI for a complete analyzis with metrics.
---

## Tech Stack
- Language: Python 3.11
- Framework: FastAPI
- AI Engine: LangChain + Groq API (Llama 3.3 70B)
- Database: PostgreSQL + SQLAlchemy 2.0 (Async)
- Migrations: Alembic
- Validation: Pydantic V2
- Server: Uvicorn
- Testing: Pytest
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
The project includes unit and integration tests focusing on Use Cases and Domain Rules using Pytest.
---

## Project Goals
- Demonstrate production-ready Python code.
- Implement real-world AI integration beyond simple wrappers.
- Showcase mastery of Software Architecture patterns.
