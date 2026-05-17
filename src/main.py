from datetime import datetime
from dataclasses import dataclass, field
from typing import Any

import streamlit as st
from auditor.schemas import AuditResult
from auditor.auditor import SecurityAuditor
from generator.generator import SQLGenerator

# from helpers import result_formatter


@dataclass
class IterationLog:
    """Лог одной итерации."""

    timestamp: datetime
    iteration: int
    sql_query: str
    audit_result: AuditResult
    revision_notes: str = (
        ""  # Что именно было исправлено по сравнению с предыдущей итерацией
    )


@dataclass
class SystemResult:
    """Финальный результат системы."""

    final_sql: str  # Итоговый SQL-запрос
    approved: bool  # Одобрен ли финальный запрос
    iterations_used: int  # Сколько итераций потребовалось
    iterations_log: list[IterationLog]  # Полный лог всех итераций
    audit_log: str  # Человекочитаемый отчёт для аналитика
    metadata: dict[str, Any] = field(
        default_factory=dict
    )  # Любые доп. данные команды


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

    def _build_audit_log(self, iterations_log: list[IterationLog]) -> str:
        # TODO: реализовать логирование аудита
        raise NotImplementedError

    def run(self, task_description: str) -> SystemResult:
        """Input: task_description. Output: SystemResult with final SQL, approval flag and iteration log."""
        iterations_log: list[IterationLog] = []
        current_sql: str | None = None
        audit_feedback: str | None = None

        for iteration in range(1, self.max_iterations + 1):
            current_sql = self.generator.generate(
                task_description=task_description,
                iteration=iteration,
                previous_sql=current_sql,
                audit_feedback=audit_feedback,
            )

            audit_result = self.auditor.audit(
                sql_query=current_sql,
                db_schema=self.generator.db_schema,
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
                    audit_log=self._build_audit_log(iterations_log),
                    metadata={},
                )

            audit_feedback = audit_result.feedback

        return SystemResult(
            final_sql=current_sql,
            approved=False,
            iterations_used=self.max_iterations,
            iterations_log=iterations_log,
            audit_log=self._build_audit_log(iterations_log),
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
    auditor = SecurityAuditor(**(auditor_kwargs or {}))
    system = SQLSecuritySystem(
        generator=generator, auditor=auditor, max_iterations=max_iterations
    )
    return system.run(task_description=task_description)


if __name__ == "__main__":
    st.title("GreeData: Text-to-SQL")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Введите интересующий Вас запрос"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # TODO: реализовать получение информации о связях в БД
        schema = ...

        # TODO
        # 1. Получение prompt для передачи в модель
        # 2. Здесь происходит переход на Генератор-Аудитор
        # 3. Возвращается одобренный SQL-запрос

        # result = run_sql_security_pipeline(
        #     task_description=prompt,
        #     db_schema=schema,
        # )

        # TODO: реализовать форматтер из датакласса в текст
        # res_to_text: str = result_formatter(result)
        
        res_to_text = f"Echo: {prompt}"
        with st.chat_message("assistant"):
            st.markdown(res_to_text)

        st.session_state.messages.append(
            {"role": "assistant", "content": res_to_text}
        )
