from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Engine, select, and_, func
from app.infrastructure.db.models import Sprint, Task, TaskBlocker, Decision, Project
from app.schemas.report import SprintReportResponse, SprintMetrics, BlockerSummary, DecisionSummary
from app.core.config import settings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from fastapi import HTTPException
from langchain_community.utilities import SQLDatabase
import os

class ReportService:
    def __init__(self, db_engine: Engine):
        self.engine = db_engine
        self.model_name = "llama-3.3-70b-versatile"
        
        self.db = SQLDatabase(self.engine, sample_rows_in_table_info=0)
        
        api_key = os.getenv("API_KEY") 
        
        self.llm = ChatGroq(
            temperature=0,
            model_name=self.model_name,
            api_key=api_key
        )

    async def generate_sprint_report(self, sprint_id: int) -> SprintReportResponse:
        # 1. Obtener datos del Sprint
        result = await self.db.execute(select(Sprint).where(Sprint.id == sprint_id))
        sprint = result.scalar_one_or_none()
        
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")

        # 2. Obtener Tareas del Sprint
        tasks_result = await self.db.execute(select(Task).where(Task.sprint_id == sprint_id))
        tasks = tasks_result.scalars().all()

        # 3. Calcular Métricas
        total = len(tasks)
        completed = len([t for t in tasks if t.status == "DONE"])
        in_progress = len([t for t in tasks if t.status == "IN_PROGRESS"])
        # Asumiendo que 'BLOCKED' es un status, o si tienes una logica distinta, ajustalo aqui
        blocked_status = len([t for t in tasks if t.status == "BLOCKED"]) 
        pending = len([t for t in tasks if t.status == "TODO"])

        # Calcular porcentaje (evitar división por cero)
        completion_pct = (completed / total * 100) if total > 0 else 0.0

        metrics = SprintMetrics(
            total_tasks=total,
            completed_tasks=completed,
            in_progress_tasks=in_progress,
            blocked_tasks=blocked_status,
            pending_tasks=pending,
            completion_percentage=round(completion_pct, 2)
        )

        # 4. Obtener Bloqueos Activos (join con tareas de este sprint)
        # Buscamos blockers que estén "resueltos = False" en tareas de este sprint
        blockers_query = select(TaskBlocker, Task).join(Task).where(
            and_(
                Task.sprint_id == sprint_id,
                TaskBlocker.is_resolved == False
            )
        )
        blockers_res = await self.db.execute(blockers_query)
        active_blockers_data = blockers_res.scalars().all()
        
        blockers_summary = [
            # Ojo: Accedemos a la task via lazy loading o eager loading si está configurado
            # Aquí asumo que podemos acceder a la relacion, sino ajustamos la query
            BlockerSummary(task_title=f"Task #{b.task_id}", blocker_description=b.description) 
            for b in active_blockers_data
        ]

        # 5. Obtener Decisiones (Tomadas durante las fechas del sprint para el proyecto)
        # Asumiendo que Decision tiene 'created_at' y link a 'project_id'
        decisions_query = select(Decision).where(
            and_(
                Decision.project_id == sprint.project_id,
                Decision.created_at >= sprint.start_date,
                Decision.created_at <= sprint.end_date
            )
        )
        decisions_res = await self.db.execute(decisions_query)
        decisions_data = decisions_res.scalars().all()

        decisions_summary = [
            DecisionSummary(title=d.title, status=d.status, created_at=d.created_at.date())
            for d in decisions_data
        ]

        # 6. Generar Análisis con IA (Groq)
        ai_analysis_text = await self._generate_ai_analysis(
            sprint_name=sprint.name,
            metrics=metrics,
            blockers=blockers_summary,
            decisions=decisions_summary
        )

        return SprintReportResponse(
            sprint_id=sprint.id,
            sprint_name=sprint.name,
            period_start=sprint.start_date,
            period_end=sprint.end_date,
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