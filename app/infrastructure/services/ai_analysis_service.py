from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from sqlalchemy.engine import Engine
from app.application.ports.ai_analysis_service import AIAnalysisService

from app.domain.enums import ProjectRole, SprintStatus, ObjectiveStatus, TaskStatus, BlockerStatus

class LangChainAnalysisAdapter(AIAnalysisService):
    def __init__(self, db_engine: Engine, model_name: str = "llama3"):
        self.engine = db_engine
        self.model_name = model_name
        self.db = SQLDatabase(self.engine) 
        self.llm = ChatOllama(model=model_name, temperature=0)

    def _get_domain_enums_text(self) -> str:
        """Helper para formatear los enums como texto explicativo"""
        return f"""
        VALORES VÁLIDOS PARA FILTROS (Usa solo estos strings exactos en tus WHERE clauses):
        - Sprint Status: {[e.value for e in SprintStatus]}
        - Task Status: {[e.value for e in TaskStatus]}
        - Objective Status: {[e.value for e in ObjectiveStatus]}
        - Blocker Status: {[e.value for e in BlockerStatus]}
        - Project Role: {[e.value for e in ProjectRole]}
        
        NOTA: Si el usuario pregunta por "tareas terminadas" o "listas", usa 'completed'.
        Si pregunta por "tareas activas" o "en curso", usa 'in_progress'.
        """

    def analyze_project(self, project_id: int, question: str) -> str:
        generate_query_chain = create_sql_query_chain(self.llm, self.db)
        execute_query = QuerySQLDataBaseTool(db=self.db)

        answer_prompt = PromptTemplate.from_template(
            """Eres un experto Project Manager asistido por IA.
            Dada la pregunta del usuario, la consulta SQL y el resultado, responde en español.
            
            Pregunta: {question}
            SQL Query: {query}
            SQL Result: {result}
            
            Respuesta:"""
        )

        chain = (
            RunnablePassthrough.assign(query=generate_query_chain)
            .assign(result=itemgetter("query") | execute_query)
            | answer_prompt
            | self.llm
            | StrOutputParser()
        )

        # Contexto enriquecido
        today = datetime.now().strftime("%Y-%m-%d")
        enums_info = self._get_domain_enums_text()

        full_prompt = (
            f"Hoy es {today}. Contexto: project_id = {project_id}. "
            f"{enums_info}\n"
            f"Instrucción: Genera una query SQL para responder: '{question}'. "
            f"Asegúrate de filtrar siempre por project_id={project_id}."
        )

        response = chain.invoke({
            "question": full_prompt,
            "project_id": project_id 
        })
        
        return response