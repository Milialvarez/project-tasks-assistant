from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy.engine import Engine
from app.application.ports.ai_analysis_service import AIAnalysisService
from app.domain.enums import SprintStatus, ObjectiveStatus, TaskStatus

class LangChainAnalysisAdapter(AIAnalysisService):
    def __init__(self, db_engine: Engine, model_name: str = "llama3.2:1b"): 
        self.engine = db_engine
        self.model_name = model_name
        self.db = SQLDatabase(self.engine, sample_rows_in_table_info=0) 
        
        self.llm = ChatOllama(
            model=model_name, 
            temperature=0,
            stop=[";", "```"] 
        )

    def _get_domain_enums_text(self) -> str:
        return f"""
        VALORES VÁLIDOS:
        - Sprint: {[e.value for e in SprintStatus]}
        - Task: {[e.value for e in TaskStatus]}
        - Objective: {[e.value for e in ObjectiveStatus]}
        """

    def _get_minimal_schema(self, table_names: list) -> str:
        """
        Crea una representación MINIMALISTA de la base de datos.
        En lugar de 'CREATE TABLE...', devuelve 'tabla: col1, col2, col3'.
        Esto reduce el prompt de 10k caracteres a unos pocos cientos.
        """
        schema_summary = []
        try:
            # Usamos el inspector de SQLAlchemy directamente para ser rápidos
            inspector = self.db._inspector
            
            for table in table_names:
                # Solo obtenemos nombres de columnas, ignoramos tipos para ahorrar tokens
                columns = [col['name'] for col in inspector.get_columns(table)]
                schema_summary.append(f"- Table '{table}' has columns: {', '.join(columns)}")
                
            return "\n".join(schema_summary)
        except Exception as e:
            # Fallback por si algo falla
            print(f"Error generando esquema minimalista: {e}")
            return self.db.get_table_info(table_names)

    def analyze_project(self, project_id: int, question: str) -> str:
        print("--- [1] Iniciando (Modo Rápido) ---")

        # 1. FILTRO MANUAL DE TABLAS (Solo las críticas)
        # Ajusta estos nombres si en tu BD son plurales o singulares
        target_tables = ["projects", "sprint", "task", "objective", "task_status_history", "decisions", "project_members"]
        
        # 2. Obtener esquema optimizado
        # Esto bajará de 10,000 chars a ~500 chars
        db_schema = self._get_minimal_schema(target_tables)
        print(f"--- [2] Longitud del esquema optimizado: {len(db_schema)} caracteres ---")

        enums_text = self._get_domain_enums_text()

        # 3. Prompt Simplificado
        template = f"""You are a SQL expert. Convert the user question into a PostgreSQL query.
        Return ONLY the raw SQL. No markdown, no explanations.
        
        Tables Schema:
        {{schema}}

        Valid Status Values:
        {enums_text}

        Rules:
        - Filter by project_id = {project_id}
        - Use ILIKE for text search.
        - Limit to {{top_k}} rows if no number specified.
        
        Question: {{input}}
        SQL:"""

        sql_prompt = PromptTemplate.from_template(template)
        
        # 4. Generación SQL (Ahora debería volar 🚀)
        print("--- [3] Generando SQL... ---")
        sql_generator = sql_prompt | self.llm | StrOutputParser()
        
        generated_sql = sql_generator.invoke({
            "input": question,
            "top_k": 5,
            "schema": db_schema # Pasamos el esquema ligero
        })

        clean_sql = generated_sql.strip().replace("```sql", "").replace("```", "").strip()
        print(f"--- [DEBUG] SQL: {clean_sql} ---")

        # 5. Ejecución
        try:
            sql_result = self.db.run(clean_sql)
        except Exception as e:
            return f"Error SQL: {e}"

        # 6. Respuesta final
        # Usamos un prompt muy corto para que la respuesta final también sea rápida
        answer_prompt = PromptTemplate.from_template(
            "Data: {result}\nQuestion: {question}\nAnswer in Spanish as a Project Manager based strictly on the data:"
        )

        print("--- [4] Interpretando respuesta... ---")
        final_chain = answer_prompt | self.llm | StrOutputParser()

        response = final_chain.invoke({
            "question": question,
            "result": sql_result
        })
        
        return response