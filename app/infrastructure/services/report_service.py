import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from fastapi import HTTPException
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.domain.enums import TaskStatus
from app.infrastructure.db.models import Sprint, Task, TaskBlocker, Decision
from app.schemas.report import SprintReportResponse, SprintMetrics, BlockerSummary, DecisionSummary

class ReportService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.model_name = "llama-3.3-70b-versatile"
        
        api_key = os.getenv("API_KEY")
        
        self.llm = ChatGroq(
            temperature=0,
            model_name=self.model_name,
            api_key=api_key
        )

    async def generate_sprint_report(self, sprint_id: int) -> SprintReportResponse:
        
        result = self.db.execute(select(Sprint).where(Sprint.id == sprint_id))
        sprint = result.scalar_one_or_none()
        
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")

        tasks_result = self.db.execute(select(Task).where(Task.sprint_id == sprint_id))
        tasks = tasks_result.scalars().all()

        total = len(tasks)
        completed = len([t for t in tasks if t.current_status == TaskStatus.completed])
        in_progress = len([t for t in tasks if t.current_status == TaskStatus.in_progress])
        blocked_status = len([t for t in tasks if t.current_status == TaskStatus.blocked]) 
        pending = len([t for t in tasks if t.current_status == TaskStatus.pending])

        completion_pct = (completed / total * 100) if total > 0 else 0.0

        metrics = SprintMetrics(
            total_tasks=total,
            completed_tasks=completed,
            in_progress_tasks=in_progress,
            blocked_tasks=blocked_status,
            pending_tasks=pending,
            completion_percentage=round(completion_pct, 2)
        )

        blockers_query = select(TaskBlocker, Task).join(Task).where(
            and_(
                Task.sprint_id == sprint_id,
                TaskBlocker.solved_at == None 
            )
        )
        blockers_res = self.db.execute(blockers_query)
        blockers_data = blockers_res.all() 
        
        blockers_summary = []
        for row in blockers_data:
            blocker = row[0] 
            blockers_summary.append(
                BlockerSummary(task_title=f"Task #{blocker.task_id}", blocker_description=blocker.cause)
            )

        query_end_date = sprint.ended_at if sprint.ended_at else datetime.now()

        decisions_query = select(Decision).where(
            and_(
                Decision.project_id == sprint.project_id,
                Decision.created_at >= sprint.started_at,
                Decision.created_at <= query_end_date
            )
        )
        decisions_res = self.db.execute(decisions_query)
        decisions_data = decisions_res.scalars().all()

        decisions_summary = [
            DecisionSummary(title=d.title, context=d.context, impact=d.impact, created_at=d.created_at.date(), chosen_by=d.chosen_by)
            for d in decisions_data
        ]

        ai_analysis_text = await self._generate_ai_analysis(
            sprint_name=sprint.name,
            metrics=metrics,
            blockers=blockers_summary,
            decisions=decisions_summary
        )

        resp_start = sprint.started_at.date() if isinstance(sprint.started_at, datetime) else sprint.started_at
        resp_end = sprint.ended_at.date() if sprint.ended_at and isinstance(sprint.ended_at, datetime) else None

        return SprintReportResponse(
            sprint_id=sprint.id,
            sprint_name=sprint.name,
            period_start=resp_start,
            period_end=resp_end if resp_end else resp_start, 
            metrics=metrics,
            active_blockers=blockers_summary,
            decisions_made=decisions_summary,
            ai_analysis=ai_analysis_text
        )

    async def _generate_ai_analysis(self, sprint_name, metrics, blockers, decisions):
        prompt = ChatPromptTemplate.from_template("""
            Eres un Asistente experto en Gestión de Proyectos Ágiles.
            Analiza los siguientes datos del Sprint '{sprint_name}' y genera un resumen ejecutivo breve (máximo 1 párrafo y 3 puntos clave).
            
            DATOS:
            - Completitud: {completion_pct}% ({completed}/{total} tareas).
            - En Progreso: {in_progress}.
            - Pendientes: {pending}.
            - Bloqueos Activos: {blockers_count} ({blockers_desc}).
            - Decisiones Clave tomadas: {decisions_count}.

            TU TAREA:
            1. Evalúa la salud del sprint (¿Vamos bien, atrasados o en riesgo?).
            2. Menciona los bloqueos críticos si los hay.
            3. Da una recomendación accionable.
            
            Responde en formato Markdown limpio.
        """)

        chain = prompt | self.llm
        
        blockers_text = ", ".join([b.blocker_description for b in blockers]) if blockers else "Ninguno"

        response = await chain.ainvoke({
            "sprint_name": sprint_name,
            "completion_pct": metrics.completion_percentage,
            "completed": metrics.completed_tasks,
            "total": metrics.total_tasks,
            "in_progress": metrics.in_progress_tasks,
            "pending": metrics.pending_tasks,
            "blockers_count": len(blockers),
            "blockers_desc": blockers_text,
            "decisions_count": len(decisions)
        })

        return response.content