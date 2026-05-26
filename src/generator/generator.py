import re
from typing import Any

from ollama import Client

from auditor.schemas import AuditResult
from config import conf


class SQLGenerator:
    """Генерирует SQL по текстовому описанию задачи."""

    def __init__(
        self, db_schema: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        self.db_schema = db_schema or {}
        self.kwargs = kwargs

    def generate(
        self,
        task_description: str,
        sql_history: list[str],
        audit_feedback: AuditResult | None = None,
        iteration: int = 1,
    ) -> str:
        """Input: task_description/sql_history/audit_feedback/iteration. Output: SQL string."""

        ollama_client = Client(host=f"{conf.ollama_conf.model_dsn}")

        prompt = f"""Ты — генератор SQL запросов для PostgreSQL.

            Схема базы данных:
            {self.db_schema}

            {f"Замечания аудитора (исправь их): {audit_feedback}" if audit_feedback else ""}

            Задача: {task_description}

            Правила:
            1. Используй только таблицы и колонки из схемы выше
            2. Не выдумывай несуществующие таблицы
            3. Возвращай ТОЛЬКО SQL запрос, без пояснений
            4. Завершай запрос точкой с запятой
            5. Не используй markdown-разметку (```sql)

            SQL запрос:"""

        response = ollama_client.chat(
            model=conf.ollama_conf.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0,
                "num_predict": 512,
            },
        )

        content = response["message"]["content"].strip()
        content = re.sub(r"^```sql\n?", "", content)
        content = re.sub(r"\n?```$", "", content)

        sql_history.append((iteration, content))

        return content
