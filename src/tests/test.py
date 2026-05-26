import json
from typing import Any

from constants import BASEDIR
from main import SQLparser, run_sql_security_pipeline
from vector_db import search_tables

sql_parser = SQLparser()

with open(BASEDIR / "tests/requests_sample.json", "r", encoding="utf-8") as f:
    data = json.load(f)

safe_query_examples: list[dict[str, Any]] = data.get("safe_examples")
vuln_query_examples: list[dict[str, Any]] = data.get("vulnerable_examples")

safe_examples_res = []
for example in safe_query_examples:
    true_sql = example.get("sql")
    query = example.get("description")

    schema = search_tables(query=query)

    ddl_parts = []
    for table in schema:
        ddl_parts.append(table["create_table_sql"])
        if table.get("description"):
            ddl_parts.append(f"-- {table['description']}")

    schema_ddl = "\n\n".join(ddl_parts)

    sys_res = run_sql_security_pipeline(
        task_description=query,
        db_schema=schema_ddl,
    )

    pred_sql = sys_res.final_sql
    equal_res = sql_parser.compare_sql(pred_sql, true_sql)

    safe_examples_res.append(equal_res)

vuln_examples_res = []
for example in vuln_query_examples:
    true_sql = example.get("fix_sql")
    query = example.get("description")

    schema = search_tables(query=query)

    ddl_parts = []
    for table in schema:
        ddl_parts.append(table["create_table_sql"])
        if table.get("description"):
            ddl_parts.append(f"-- {table['description']}")

    schema_ddl = "\n\n".join(ddl_parts)

    sys_res = run_sql_security_pipeline(
        task_description=query,
        db_schema=schema_ddl,
    )

    pred_sql = sys_res.final_sql
    equal_res = sql_parser.compare_sql(pred_sql, true_sql)

    vuln_examples_res.append(equal_res)

safe_accuracy = sum(safe_examples_res) / len(safe_examples_res)
vuln_accuracy = sum(vuln_examples_res) / len(vuln_examples_res)

total_accuracy = (sum(safe_examples_res) + sum(vuln_examples_res)) / (
    len(safe_examples_res) + len(vuln_examples_res)
)

print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
print("=" * 50)
print(f"  Accuracy: {safe_accuracy * 100:.2f}%")
print(f"  Accuracy: {vuln_accuracy * 100:.2f}%")
print(f"Total Execution Accuracy: {total_accuracy * 100:.2f}%")
print("=" * 50)
