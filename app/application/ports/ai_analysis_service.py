# app/application/ports/ai_analysis_service.py
from abc import ABC, abstractmethod

class AIAnalysisService(ABC):
    @abstractmethod
    def analyze_project(self, project_id: int, question: str) -> str:
        """
        Recibe un ID de proyecto y una pregunta natural.
        Retorna una respuesta en texto natural basada en los datos.
        """
        pass