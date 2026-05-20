from typing import Any

from ollama import Client
from auditor.schemas import AuditResult
from config import conf

ollama_client = Client(host=f"{conf.ollama_conf.model_dsn}")


class SQLGenerator:
    """Генерирует SQL по текстовому описанию задачи."""

    def __init__(
        self, db_schema: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        self.db_schema = db_schema or {}
        self.kwargs = kwargs

        self.ollama_client = Client(host=f"{conf.ollama_conf.model_dsn}")
        self.model_name = conf.ollama_conf.MODEL_NAME

    def generate(
        self,
        task_description: str,
        sql_history: list[str] | None = None,
        audit_feedback: AuditResult | None = None,
        iteration: int = 1,
    ) -> str:
        """Input: task_description/sql_history/audit_feedback/iteration. Output: SQL string."""
        
        prompt = f"""### Task
            Generate a SQL query to answer [QUESTION]{task_description}[/QUESTION]

            ### Database Schema
            The query will run on a database with the following schema:
            {self.db_schema}

            ### Answer
            Given the database schema, here is the SQL query that answers [QUESTION]{task_description}[/QUESTION]
            [SQL]"""

        response = ollama_client.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response["message"]["content"]
