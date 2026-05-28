from dataclasses import dataclass, field
from datetime import datetime
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

    def build_audit_log(self, iterations_log: list[IterationLog]) -> str:
        """Формирует человекочитаемый лог аудита"""
        lines = []
        lines.append("=" * 20)
        lines.append("Аудит безопасности SQL")
        lines.append("=" * 20)
        lines.append(f"Всего итераций: {len(iterations_log)}")
        lines.append("")

        for log in iterations_log:
            lines.append(f"\n{'─' * 20}")
            lines.append(f"Итерация #{log.iteration}")
            lines.append(f"{'─' * 20}")

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

        lines.append("=" * 20)
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

        lines.append("=" * 20)

        return "\n".join(lines)

    def run(self, task_description: str) -> SystemResult:
        """Input: task_description. Output: SystemResult with final SQL, approval flag and iteration log."""
        iterations_log: list[IterationLog] = []
        current_sql: str | None = None
        audit_feedback: str | None = None
        sql_history: list[str] = []

        prev_sql = None
        repeat_count = 0
        warning_prompt = ""

        for iteration in range(1, self.max_iterations + 1):
            current_sql = self.generator.generate(
                task_description=task_description,
                sql_history=sql_history,
                iteration=iteration,
                audit_feedback=audit_feedback,
            )

            if prev_sql and self.sql_parser.compare_sql(prev_sql, current_sql):
                repeat_count += 1

                if repeat_count >= 2:
                    return SystemResult(
                        final_sql=current_sql,
                        approved=False,
                        iterations_used=iteration,
                        iterations_log=iterations_log,
                        audit_log=self.build_audit_log(iterations_log),
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

            iter_log = IterationLog(
                timestamp=datetime.now(),
                iteration=iteration,
                sql_query=current_sql,
                audit_result=audit_result,
                revision_notes=audit_feedback or "Первая генерация",
            )
            iterations_log.append(iter_log)

            if audit_result.approved:
                return SystemResult(
                    final_sql=current_sql,
                    approved=True,
                    iterations_used=iteration,
                    iterations_log=iterations_log,
                    audit_log=self.build_audit_log(iterations_log),
                    metadata={},
                )

            audit_feedback = warning_prompt + audit_result.feedback

        return SystemResult(
            final_sql=current_sql,
            approved=False,
            iterations_used=iteration,
            iterations_log=iterations_log,
            audit_log=self.build_audit_log(iterations_log),
            metadata={
                "warning": "Достигнут лимит итераций",
            },
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


# if __name__ == "__main__":
#     st.title("GreeData: Text-to-SQL")

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if prompt := st.chat_input("Введите интересующий Вас запрос"):
#         st.chat_message("user").markdown(prompt)
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         schema = search_tables(query=prompt)

#         ddl_parts = []
#         for table in schema:
#             ddl_parts.append(table["create_table_sql"])
#             if table.get("description"):
#                 ddl_parts.append(f"-- {table['description']}")

#         schema_ddl = "\n\n".join(ddl_parts)

#         result = run_sql_security_pipeline(
#             task_description=prompt,
#             db_schema=schema_ddl,
#         )

#         res_to_text = (
#             f"{'Одобрен\n' if result.approved else 'Внимание! Скрипт не прошел проверку аудитором\n'}"
#             f"Полученный SQL-скрипт:\n{result.final_sql}\n\n"
#             f"\nЧеловекочитаемый лог итераций:\n{result.audit_log}\n"
#         )
        
#         total_sql = sql_parser.format_sql(result.final_sql)
        
#         with st.chat_message("assistant"):
#             if result.approved:
#                 st.success("✅ SQL ОДОБРЕН")
#             else:
#                 st.error("⚠️ ВНИМАНИЕ! Скрипт не прошел проверку аудитором")
            
#             with st.expander("Сгенерированный SQL", expanded=True):
#                 st.code(total_sql, language="sql")
            
#             with st.expander("Лог аудита (подробно)", expanded=False):
#                 st.text(result.audit_log)

#         st.session_state.messages.append(
#             {"role": "assistant", "content": res_to_text}
#         )
