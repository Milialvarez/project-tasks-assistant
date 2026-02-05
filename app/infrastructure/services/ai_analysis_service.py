import os
from langchain_groq import ChatGroq 
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy.engine import Engine
from app.application.ports.ai_analysis_service import AIAnalysisService
from app.domain.enums import SprintStatus, ObjectiveStatus, TaskStatus

class LangChainAnalysisAdapter(AIAnalysisService):
    def __init__(self, db_engine: Engine):
        self.engine = db_engine
        # Usamos el modelo Llama 3 70B (versión potente) o 8B (rápida).
        # Groq es tan rápido que puedes usar el 70b-8192 sin problemas.
        self.model_name = "llama-3.3-70b-versatile"
        
        # sample_rows=0 sigue siendo buena práctica
        self.db = SQLDatabase(self.engine, sample_rows_in_table_info=0)
        
        # CONFIGURACIÓN GROQ
        # Lo ideal es leer esto de os.environ.get("GROQ_API_KEY")
        # Pero pégala aquí para probar YA MISMO.
        api_key = os.getenv("API_KEY")
        
        self.llm = ChatGroq(
            temperature=0,
            model_name=self.model_name,
            api_key=api_key
        )

    def _get_domain_enums_text(self) -> str:
        return f"""
        VALORES VÁLIDOS:
        - Sprint: {[e.value for e in SprintStatus]}
        - Task: {[e.value for e in TaskStatus]}
        - Objective: {[e.value for e in ObjectiveStatus]}
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

    def analyze_project(self, project_id: int, question: str) -> str:
        # 1. Filtro de tablas
        target_tables = ["projects", "sprint", "task", "objective", "task_status_history", "decisions", "project_members", "users", "task_blocker"]
        
        # 2. Esquema
        db_schema = self._get_minimal_schema(target_tables)

        # 3. Prompt SQL
        template = f"""You are a SQL expert using PostgreSQL.
        Given an input question, create a syntactically correct PostgreSQL query to run.
        Return ONLY the raw SQL query. Do not use markdown blocks. Do not add explanations.
        
        Schema:
        {{schema}}

        Enums:
        {self._get_domain_enums_text()}

        Constraints:
        - Filter by project_id = {project_id}
        - Use ILIKE for text search
        - Limit to {{top_k}} results if unspecified
        
        Question: {{input}}
        SQL Query:"""

        sql_prompt = PromptTemplate.from_template(template)
        
        # Generación
        sql_generator = sql_prompt | self.llm | StrOutputParser()
        
        try:
            generated_sql = sql_generator.invoke({
                "input": question,
                "top_k": 5,
                "schema": db_schema
            })
            
            # Limpieza básica por si acaso
            clean_sql = generated_sql.strip().replace("```sql", "").replace("```", "").strip()
            # A veces Groq devuelve "Here is the SQL: SELECT...", quitamos el preámbulo si existe
            if "SELECT" in clean_sql:
                clean_sql = clean_sql[clean_sql.find("SELECT"):]
            
            print(f"DEBUG SQL: {clean_sql}")
            
            # Ejecución
            sql_result = self.db.run(clean_sql)
            
            # Respuesta Final
            answer_prompt = PromptTemplate.from_template(
                "Data: {result}\nQuestion: {question}\nAnswer concisely in Spanish as a Project Manager:"
            )
            
            final_chain = answer_prompt | self.llm | StrOutputParser()
            
            return final_chain.invoke({
                "question": question,
                "result": sql_result
            })

        except Exception as e:
            return f"Error procesando la solicitud: {str(e)}"