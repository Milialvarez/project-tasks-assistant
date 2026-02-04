from langchain_community.llms import Ollama


class OllamaClient:
    def __init__(self, model: str = "llama3"):
        self.llm = Ollama(model=model)

    def explain_delays(self, analytics_summary: dict) -> str:
        prompt = f"""
You are an agile project assistant.

Based on the following project data, explain:
- Why tasks are delayed
- Main blockers
- Which tasks need attention

Be clear, concise and professional.
Do NOT invent data.

Project data:
{analytics_summary}
"""
        return self.llm.invoke(prompt)
