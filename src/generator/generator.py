import re
from typing import Any

from ollama import Client
from openai import OpenAI

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
    ) -> tuple[str, int]:
        """Input: task_description/sql_history/audit_feedback/iteration. Output: SQL string."""

        client = OpenAI(
            base_url=conf.ollama_conf.model_dsn,
            api_key="ollama",
        )

        prompt = f"""Ты — генератор SQL запросов для PostgreSQL.

            Схема базы данных:
            {self.db_schema}

            {f"Замечания аудитора (исправь их): {audit_feedback}" if audit_feedback else ""}

            Задача: {task_description}

            Правила:
            1. Используй только таблицы и колонки из схемы выше
            2. Не выдумывай несуществующие таблицы
            3. Используй конкретные поля вместо *
            3. Всегда используй LIMIT, где это уместно
            4. Возвращай ТОЛЬКО SQL запрос, без пояснений
            6. Завершай запрос точкой с запятой
            7. Не используй markdown-разметку (```sql)

            SQL запрос:"""

        response = client.chat.completions.create(
            model=conf.ollama_conf.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )

        tokens_used = response.usage.total_tokens

        content = response.choices[0].message.content.strip()
        content = re.sub(r"^```sql\n?", "", content)
        content = re.sub(r"\n?```$", "", content)

        sql_history.append((iteration, content))

        return content, tokens_used
