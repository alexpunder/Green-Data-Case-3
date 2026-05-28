from dataclasses import dataclass, field
from datetime import datetime
from time import perf_counter
from typing import Any

from auditor.auditor import SecurityAuditor
from auditor.schemas import AuditResult
from generator.generator import SQLGenerator
from sql_parser import sql_parser


@dataclass
class IterationLog:
    """Лог одной итерации."""

    timestamp: datetime
    iteration: int
    sql_query: str
    audit_result: AuditResult
    revision_notes: str = ""

    @property
    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "iteration": self.iteration,
            "sql_query": self.sql_query,
            "audit_result": self.audit_result.to_dict,
            "revision_notes": self.revision_notes,
        }


@dataclass
class SystemResult:
    """Финальный результат системы."""

    final_sql: str
    approved: bool
    iterations_used: int
    iterations_log: list[IterationLog]
    audit_log: str
    total_tokens_used: int
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def to_dict(self):
        return {
            "final_sql": self.final_sql,
            "approved": self.approved,
            "iterations_used": self.iterations_used,
            "iterations_log": [
                iteration_log.to_dict for iteration_log in self.iterations_log
            ],
            "audit_log": self.audit_log,
            "total_tokens_used": self.total_tokens_used,
            "metadata": self.metadata,
        }


class SQLSecuritySystem:
    """Оркестрирует цикл генерация -> аудит -> исправление."""

    DEFAULT_MAX_ITERATIONS = 5

    def __init__(
        self,
        generator: SQLGenerator,
        auditor: SecurityAuditor,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
    ) -> None:
        self.generator = generator
        self.auditor = auditor
        self.max_iterations = max_iterations
        self.sql_parser = sql_parser

    def build_audit_log(self, iterations_log: list[IterationLog], total_tokens: int, timer: float) -> str:
        """Формирует человекочитаемый лог аудита"""
        lines = []
        lines.append("=" * 40)
        lines.append("Аудит безопасности SQL")
        lines.append("=" * 40)
        lines.append(f"Всего итераций:         {len(iterations_log)}")
        lines.append(f"Всего токенов:          {total_tokens:,}")
        lines.append(f"Среднее токенов:        {total_tokens / len(iterations_log):.0f}")
        lines.append(f"Общее время:            {timer:.2f} сек.")
        lines.append(f"Среднее время/итерация: {timer / len(iterations_log):.2f} сек.")
        lines.append("")

        for log in iterations_log:
            lines.append(f"\n{'─' * 40}")
            lines.append(f"Итерация #{log.iteration}")
            lines.append(f"{'─' * 40}")

            sql_preview = log.sql_query[:300]
            if len(log.sql_query) > 300:
                sql_preview += "..."
            lines.append(f"\nSQL запрос:\n{sql_preview}")

            audit = log.audit_result
            status = "Одобрено" if audit.approved else "Отклонено"
            lines.append(f"\nРезультат: {status}")
            lines.append(f"Риск: {audit.overall_risk_score:.2f}/10.0")

            if audit.summary:
                lines.append(f"Вердикт: {audit.summary}")

            if audit.vulnerabilities:
                lines.append("\nНайденные проблемы:")
                for v in audit.vulnerabilities:
                    lines.append(
                        f"  • {v.vuln_class} (риск: {v.risk_score}/10)"
                    )
                    lines.append(f"    {v.description[:150]}")
                    if v.recommendation:
                        lines.append(f"    {v.recommendation[:150]}")

            if log.revision_notes and log.revision_notes != "Первая генерация":
                lines.append(f"\nFeedback генератору: {log.revision_notes}")

            lines.append("")

        lines.append("=" * 40)
        final_approved = (
            iterations_log[-1].audit_result.approved
            if iterations_log
            else False
        )

        if final_approved:
            lines.append("Итоговый результат: SQL одобрен")
            lines.append(f"   Финальный SQL:\n{iterations_log[-1].sql_query}")
        else:
            lines.append("Итоговый результат: SQL не одобрен")
            lines.append(
                f"   Причина: {iterations_log[-1].audit_result.summary if iterations_log else 'Нет данных'}"
            )

        lines.append("=" * 40)

        return "\n".join(lines)

    def run(self, task_description: str) -> SystemResult:
        """Input: task_description. Output: SystemResult with final SQL, approval flag and iteration log."""
        start_time = perf_counter()
        
        iterations_log: list[IterationLog] = []
        current_sql: str | None = None
        audit_feedback: str | None = None
        sql_history: list[str] = []
        total_tokens_used: int = 0

        prev_sql = None
        repeat_count = 0
        warning_prompt = ""

        for iteration in range(1, self.max_iterations + 1):
            current_sql, tokens_used = self.generator.generate(
                task_description=task_description,
                sql_history=sql_history,
                iteration=iteration,
                audit_feedback=audit_feedback,
            )
            total_tokens_used += tokens_used

            if prev_sql and self.sql_parser.compare_sql(prev_sql, current_sql):
                repeat_count += 1

                if repeat_count >= 2:
                    
                    end_time = perf_counter()
                    
                    return SystemResult(
                        final_sql=current_sql,
                        approved=False,
                        iterations_used=iteration,
                        iterations_log=iterations_log,
                        audit_log=self.build_audit_log(
                            iterations_log,
                            total_tokens_used,
                            end_time - start_time,
                        ),
                        total_tokens_used=total_tokens_used,
                        metadata={
                            "warning": "Генератор повторяет один и тот же SQL без исправлений"
                        },
                    )

                warning_prompt = (
                    f"Ты уже отправлял этот SQL на итерации {iteration - 1}! "
                    "Он был отклонён. НЕ ПОВТОРЯЙ ЕГО!"
                )

            else:
                repeat_count = 0
                warning_prompt = ""

            prev_sql = current_sql

            audit_result = self.auditor.audit(
                sql_query=current_sql,
            )
            total_tokens_used += audit_result.tokens_used

            iter_log = IterationLog(
                timestamp=datetime.now(),
                iteration=iteration,
                sql_query=current_sql,
                audit_result=audit_result,
                revision_notes=audit_feedback or "Первая генерация",
            )
            iterations_log.append(iter_log)

            if audit_result.approved:
                
                end_time = perf_counter()
                
                return SystemResult(
                    final_sql=current_sql,
                    approved=True,
                    iterations_used=iteration,
                    iterations_log=iterations_log,
                    audit_log=self.build_audit_log(
                        iterations_log,
                        total_tokens_used,
                        end_time - start_time,
                    ),
                    total_tokens_used=total_tokens_used,
                    metadata={},
                )

            audit_feedback = warning_prompt + audit_result.feedback

        end_time = perf_counter()

        return SystemResult(
            final_sql=current_sql,
            approved=False,
            iterations_used=iteration,
            iterations_log=iterations_log,
            audit_log=self.build_audit_log(
                iterations_log,
                total_tokens_used,
                end_time - start_time,
            ),
            total_tokens_used=total_tokens_used,
            metadata={"warning": "Достигнут лимит итераций"},
        )


def run_sql_security_pipeline(
    task_description: str,
    db_schema: dict[str, Any] | None = None,
    max_iterations: int = SQLSecuritySystem.DEFAULT_MAX_ITERATIONS,
    generator_kwargs: dict[str, Any] | None = None,
    auditor_kwargs: dict[str, Any] | None = None,
) -> SystemResult:
    """Main entrypoint.

    Input:
    - task_description: natural language task.
    - db_schema: machine-readable DB schema.
    - max_iterations: iteration limit for generator->auditor loop.
    - generator_kwargs/auditor_kwargs: optional params for custom implementations.

    Output:
    - SystemResult.
    """
    generator = SQLGenerator(
        db_schema=db_schema or {}, **(generator_kwargs or {})
    )
    auditor = SecurityAuditor(
        db_schema=db_schema or {}, **(auditor_kwargs or {})
    )
    system = SQLSecuritySystem(
        generator=generator, auditor=auditor, max_iterations=max_iterations
    )
    return system.run(task_description=task_description)
