# generator/generator.py
import os
import re
from openai import OpenAI


class SQLGenerator:
    """Генерирует SQL запросы через DeepSeek API."""

    def __init__(self, db_schema: str = ""):
        self.db_schema = db_schema
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        )
        self.model = "deepseek-chat"

    def generate(
        self,
        task_description: str,
        sql_history: list = None,
        iteration: int = 1,
        audit_feedback: str = None,
        similar_errors: list = None,
    ) -> str:
        """Генерирует SQL запрос на основе описания и фидбека от аудитора."""
        
        system_prompt = f"""Ты — эксперт по генерации безопасных SQL запросов для PostgreSQL.

СХЕМА БАЗЫ ДАННЫХ:
{self.db_schema}

ПРАВИЛА:
1. НИКОГДА не используй SELECT *
2. ВСЕГДА добавляй LIMIT
3. Используй параметризацию (%s)
4. Не запрашивай чувствительные поля без необходимости
"""

        user_prompt = f"ЗАДАЧА: {task_description}\n\n"

        # Добавляем историю предыдущих попыток
        if sql_history:
            user_prompt += "ПРЕДЫДУЩИЕ ПОПЫТКИ (не повторяй ошибки):\n"
            for i, sql in enumerate(sql_history[-3:], 1):
                user_prompt += f"Попытка {i}:\n{sql}\n\n"

        # Добавляем фидбек от аудитора
        if audit_feedback:
            user_prompt += f"""
⚠️ ЗАМЕЧАНИЯ АУДИТОРА (ИСПРАВЬ ЭТИ ОШИБКИ):
{audit_feedback}
"""

        user_prompt += "\nSQL запрос:"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
        )

        sql = response.choices[0].message.content.strip()
        sql = re.sub(r"```sql\n?|```", "", sql)
        
        return sql