from dataclasses import dataclass


@dataclass
class Vulnerability:
    """Найденная уязвимость."""

    vuln_class: str  # Ключ из справочника VULN_CLASSES
    risk_score: float  # Оценка риска от 0.0 до 10.0
    description: str  # Человекочитаемое пояснение
    recommendation: str  # Конкретный совет по исправлению
    line_hint: int = (
        ""  # Необязательно: позиция в исходном SQL, где найдена проблема
    )


@dataclass
class AuditResult:
    """Результат проверки SQL."""

    approved: bool  # True — запрос прошёл проверку
    feedback: str  # Вердикт для генератора
    vulnerabilities: list[
        Vulnerability
    ]  # Список найденных уязвимостей (пусто если approved=True)
    overall_risk_score: (
        float  # Итоговый риск: 0.0 (безопасно) … 10.0 (критично)
    )
    summary: str  # Краткий вердикт для пользователя
