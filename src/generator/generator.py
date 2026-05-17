from typing import Any

from auditor.schemas import AuditResult


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
        sql_history: list[str] | None = None,
        audit_feedback: AuditResult | None = None,
        iteration: int = 1,
    ) -> str:
        """Input: task_description/sql_history/audit_feedback/iteration. Output: SQL string."""
        raise NotImplementedError("Implement SQLGenerator.generate()")
