from typing import Any

from auditor.schemas import AuditResult


class SecurityAuditor:
    """Проверяет SQL-запрос на типовые уязвимости."""

    VULN_CLASSES = {
        "SQL_INJ_CLASSIC": "SQL Injection (классический)",
        "SQL_INJ_UNION": "Union-based Injection",
        "DML_NO_WHERE": "UPDATE/DELETE без WHERE",
        "SELECT_STAR": "Избыточный SELECT *",
        "DIRECT_SENSITIVE": "Прямой доступ к чувствительным полям",
        "NO_PAGINATION": "Неограниченный LIMIT / отсутствие пагинации",
        "SQL_INJ_TIME": "Time-based blind Injection",
        "PRIV_ESCALATE": "Privilege Escalation через EXECUTE",
        "PLPGSQL_UNSAFE": "PL/pgSQL: небезопасный EXECUTE",
    }

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def audit(
        self, sql_query: str, db_schema: dict[str, Any] | None = None
    ) -> AuditResult:
        """Input: sql_query/db_schema. Output: AuditResult with vulnerabilities, risk and approval."""
        raise NotImplementedError("Implement SecurityAuditor.audit()")
