import json

from constants import BASEDIR
from main import run_sql_security_pipeline
from sql_parser import SQLparser
from vector_db import search_tables

sql_parser = SQLparser()

with open(
    BASEDIR / "src/tests/requests_sample.json", "r", encoding="utf-8"
) as f:
    data = json.load(f)

safe_examples_res = []
safe_query_examples = [promt for promt in data if promt["risk_label"] == "SAFE"]
for i, example in enumerate(safe_query_examples):
    true_sql = example.get("sql")
    query = example.get("instruction")

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

    print(
        f"Итерация номер #{i}.\n"
        f"Ген. запрос: \n{pred_sql}\n"
        "--------\n"
        f"Реал. запрос: \n{true_sql}\n"
        "--------\n"
    )

vuln_examples_res = []
vuln_query_examples = [promt for promt in data if promt["risk_label"] == "VULNERABLE"]
for i, example in enumerate(vuln_query_examples):
    true_sql = example.get("sql")
    query = example.get("instruction")

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

    print(
        f"Итерация номер #{i}.\n"
        f"Ген. запрос: \n{pred_sql}\n"
        "--------\n"
        f"Реал. запрос: \n{true_sql}\n"
        "--------\n"
    )
