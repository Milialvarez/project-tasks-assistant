import os
from langchain_groq import ChatGroq 
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy.engine import Engine
from app.application.ports.ai_analysis_service import AIAnalysisService
from app.domain.enums import BlockerStatus, SprintStatus, ObjectiveStatus, TaskStatus

class LangChainAnalysisAdapter(AIAnalysisService):
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

    def _get_domain_enums_text(self) -> str:
        return f"""
        VALORES VÁLIDOS (ENUMS):
        - Sprint Status: {[e.value for e in SprintStatus]}
        - Task Status: {[e.value for e in TaskStatus]}
        - Objective Status: {[e.value for e in ObjectiveStatus]}
        - Blocker Status : {[e.value for e in BlockerStatus]}
        """

    def _get_minimal_schema(self, table_names: list) -> str:
        schema_summary = []
        try:
            inspector = self.db._inspector
            for table in table_names:
                columns = [col['name'] for col in inspector.get_columns(table)]
                schema_summary.append(f"- Table '{table}' has columns: {', '.join(columns)}")
            return "\n".join(schema_summary)
        except Exception as e:
            return self.db.get_table_info(table_names)

    def analyze_project(self, project_id: int, question: str) -> dict:
        target_tables = [
            "projects", "sprint", "task", "objective", 
            "task_status_history", "decisions", "project_members", 
            "users", "task_blocker"
        ]
        
        db_schema = self._get_minimal_schema(target_tables)

        strategies = """
        BUSINESS RULES & STRATEGIES:
        1. IF checking for "delays", "slow progress", or "why are we late":
           - MUST query the 'task_blocker' table joined with 'task' and 'users'.
           - MUST check for tasks in the active sprint that are NOT 'completed'.
           - SELECT the blocker cause, the task title, and the user name responsible.
        
        2. IF checking for "performance" or "who works most":
           - Count 'completed' tasks grouped by 'assigned_user_id' (join with users table for names).
        
        3. GENERAL:
           - Join 'users' table using 'task.assigned_user_id = users.id' to get real names, not just IDs.
           - Active Sprint means sprint.status = 'active'.
        """

        template = f"""You are a Senior Data Analyst for Agile Projects using PostgreSQL.
        Your goal is to answer the user question based STRICTLY on the database data.
        
        Schema:
        {{schema}}

        Enums:
        {self._get_domain_enums_text()}

        {strategies}

        Constraints:
        - Filter by project_id = {project_id}
        - Use ILIKE for text search
        - Limit to {{top_k}} results if unspecified
        - Return ONLY the raw SQL query. No markdown.
        
        Question: {{input}}
        SQL Query:"""

        sql_prompt = PromptTemplate.from_template(template)
        
        sql_generator = sql_prompt | self.llm | StrOutputParser()
        
        clean_sql = "" 
        try:
            generated_sql = sql_generator.invoke({
                "input": question,
                "top_k": 5,
                "schema": db_schema
            })
            
            clean_sql = generated_sql.strip().replace("```sql", "").replace("```", "").strip()
            if "SELECT" in clean_sql:
                clean_sql = clean_sql[clean_sql.find("SELECT"):]
            
            sql_result = self.db.run(clean_sql)
            
            answer_prompt = PromptTemplate.from_template(
                """Actúa como un Scrum Master Senior experto.
                Analiza los datos SQL crudos y responde la pregunta del usuario.
                
                REGLAS DE ESTILO:
                - Sé directo y profesional.
                - Si hay bloqueos, menciona EXPLÍCITAMENTE la 'causa' y 'quién' es el responsable.
                - Si el resultado SQL está vacío (ej: []), responde: "No detecto bloqueos ni problemas registrados en los datos actuales."
                - NO des consejos genéricos como "mejorar la comunicación" a menos que los datos lo sugieran.
                - Usa formato Markdown (listas, negritas) para que sea legible.
                
                Pregunta: {question}
                Datos SQL (Resultado): {result}
                
                Tu Respuesta:"""
            )
            
            final_chain = answer_prompt | self.llm | StrOutputParser()
            
            final_answer = final_chain.invoke({
                "question": question,
                "result": sql_result
            })

            return {
                "answer": final_answer,
                "sql_used": clean_sql
            }

        except Exception as e:
            return {
                "answer": f"Lo siento, tuve un problema analizando los datos: {str(e)}",
                "sql_used": clean_sql
            }