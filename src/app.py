import streamlit as st

from main import run_sql_security_pipeline
from sql_parser import sql_parser
from vector_db import search_tables

st.title("GreenData: Text-to-SQL")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            data = message["data"]
            if data["approved"]:
                st.success("✅ SQL ОДОБРЕН")
            else:
                st.error("⚠️ ВНИМАНИЕ! Скрипт не прошел проверку аудитором")

            with st.expander("Сгенерированный SQL", expanded=True):
                st.code(data["final_sql"], language="sql")

            with st.expander("Лог аудита (подробно)", expanded=False):
                st.text(data["audit_log"])

if prompt := st.chat_input("Введите интересующий Вас запрос"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Генерация SQL запроса..."):
        schema = search_tables(query=prompt)

        ddl_parts = []
        for table in schema:
            ddl_parts.append(table["create_table_sql"])
            if table.get("description"):
                ddl_parts.append(f"-- {table['description']}")

        schema_ddl = "\n\n".join(ddl_parts)

        result = run_sql_security_pipeline(
            task_description=prompt,
            db_schema=schema_ddl,
        )

        total_sql = sql_parser.format_sql(result.final_sql)

        with st.chat_message("assistant"):
            if result.approved:
                st.success("✅ SQL ОДОБРЕН")
            else:
                st.error("⚠️ ВНИМАНИЕ! Скрипт не прошел проверку аудитором")

            with st.expander("Сгенерированный SQL", expanded=True):
                st.code(total_sql, language="sql")

            with st.expander("Лог аудита (подробно)", expanded=False):
                st.text(result.audit_log)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "data": {
                    "approved": result.approved,
                    "final_sql": total_sql,
                    "audit_log": result.audit_log,
                    "iterations_used": result.iterations_used,
                },
            }
        )
