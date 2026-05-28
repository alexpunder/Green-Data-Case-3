import json
import re
from typing import Any

from ollama import Client

from auditor.schemas import AuditResult, Vulnerability
from config import conf


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
        "DDL_DROP_TABLE": "DROP TABLE — удаление таблицы (катастрофическая операция)",
        "DDL_TRUNCATE": "TRUNCATE — очистка таблицы без возможности восстановления",
        "DDL_ALTER": "ALTER TABLE — изменение структуры таблицы",
        "MULTI_STATEMENT": "Несколько запросов в одном (SELECT; DROP) — риск инъекции",
    }
    RISK_THRESHOLD = 4.0

    def __init__(
        self, db_schema: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        self.db_schema = db_schema or {}
        self.kwargs = kwargs

    def _get_vuln_classes(self) -> str:
        """Формирование списка уязвимостей для промпта."""
        vult_points = ""
        for iter, (key, value) in enumerate(self.VULN_CLASSES.items()):
            vult_points += f"{iter}. {key}: {value}\n"
        return vult_points

    def _parse_llm_response(
        self, response_text: str
    ) -> tuple[list[Vulnerability], float, str]:
        """Парсит JSON ответ от LLM в структуры данных"""
        try:
            cleaned = re.sub(r"^```json\n?", "", response_text)
            cleaned = re.sub(r"\n?```$", "", cleaned)
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            return [], 0.0, "Не удалось распарсить ответ аудитора"

        vulnerabilities = []
        for v in data.get("vulnerabilities", []):
            severity_map = {
                "critical": 9.0,
                "high": 7.0,
                "medium": 5.0,
                "low": 2.0,
            }
            risk_score = severity_map.get(v.get("severity", "low"), 2.0)

            vulnerabilities.append(
                Vulnerability(
                    vuln_class=v.get("type", "UNKNOWN"),
                    risk_score=risk_score,
                    description=v.get("description", ""),
                    recommendation=v.get("suggestion", ""),
                )
            )

        overall_risk = data.get("risk_score", 0) / 10
        summary = data.get("summary", "")

        return vulnerabilities, overall_risk, summary

    def audit(self, sql_query: str) -> AuditResult:
        """Input: sql_query/db_schema. Output: AuditResult with vulnerabilities, risk and approval."""

        ollama_client = Client(host=f"{conf.ollama_conf.model_dsn}")

        prompt = f"""Ты — Security Auditor для SQL-запросов PostgreSQL.

            Проверь следующий SQL-запрос на наличие уязвимостей:

            SQL ЗАПРОС:
            {sql_query}

            СХЕМА БАЗЫ ДАННЫХ (только существующие таблицы и колонки):
            {self.db_schema}

            ПРОВЕРЬ НАЛИЧИЕ ЭТИХ ТИПОВ УЯЗВИМОСТЕЙ:
            {self._get_vuln_classes()}

            Правила проверки:
            1. Если запрос использует таблицу или колонку, которых нет в схеме — это уязвимость INVALID_REFERENCE
            2. Обрати внимание на конкатенацию строк (||) с потенциально пользовательскими данными
            3. Проверь кавычки — неэкранированные одинарные кавычки могут быть инъекцией

            ОТВЕТЬ ТОЛЬКО В ФОРМАТЕ JSON:
            {{
                "vulnerabilities": [
                    {{
                        "type": "SQL_INJ_CLASSIC",
                        "description": "краткое описание проблемы",
                        "severity": "critical|high|medium|low",
                        "location": "часть запроса где проблема (цитата)",
                        "suggestion": "как исправить"
                    }}
                ],
                "is_safe": true/false,
                "risk_score": 0-100,
                "summary": "краткий вывод (одна строка)"
            }}

            Если уязвимостей нет, верни "vulnerabilities": [] и "is_safe": true.
            Не добавляй пояснения вне JSON."""

        response = ollama_client.chat(
            model=conf.ollama_conf.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1},
        )

        vulns, overall_risk, summary = self._parse_llm_response(
            response["message"]["content"]
        )

        approved = len(vulns) == 0 and overall_risk < self.RISK_THRESHOLD

        feedback = ""
        if not approved:
            feedback = (
                f"Найдены проблемы: {', '.join([v.vuln_class for v in vulns])}"
            )

        return AuditResult(
            approved=approved,
            feedback=feedback,
            vulnerabilities=vulns,
            overall_risk_score=overall_risk,
            summary=summary,
        )
