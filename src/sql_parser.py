import json
import re
from typing import Any

from pglast import parse_sql

from constants import BASEDIR, PATTERN_MAP


class SQLparser:
    def get_ast_root(self, sql: str):
        """Разбирает SQL и возвращает корневой узел AST."""
        if not sql:
            return None

        try:
            return parse_sql(sql)[0].stmt
        except Exception as e:
            print(f"Ошибка парсинга SQL: {e}")
            return None

    def compare_sql(self, generated: str, expected: str) -> bool:
        """Сравнивает два SQL запроса через их AST."""
        ast_gen = self.get_ast_root(generated)
        ast_exp = self.get_ast_root(expected)

        if ast_gen is None or ast_exp is None:
            return generated.strip() == expected.strip()

        return ast_gen == ast_exp

    def parse_sql_complete(self, sql_file_path: str) -> dict[str, Any]:
        """Извлекает COMMENT ON TABLE, COMMENT ON COLUMN и FOREIGN KEY из SQL-дампа"""

        with open(sql_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tables = {}

        for match in re.finditer(
            PATTERN_MAP["create_ddl"], content, re.DOTALL
        ):
            full_ddl = match.group(1)
            table_name = match.group(2)

            tables[table_name] = {
                "create_table_sql": full_ddl,
                "description": "",
                "column_comments": {},
                "foreign_keys": [],
            }

        for match in re.finditer(PATTERN_MAP["comment_on_table"], content):
            table_name = match.group(1)
            comment = match.group(2)
            clean_comment = comment.split(",")[0].strip()

            if table_name in tables:
                tables[table_name]["description"] = clean_comment

        for match in re.finditer(PATTERN_MAP["comment_on_column"], content):
            table_name = match.group(1)
            column_name = match.group(2)
            comment = match.group(3)
            clean_comment = comment.split(",")[0].strip()

            if table_name in tables:
                tables[table_name]["column_comments"][column_name] = (
                    clean_comment
                )

        for match in re.finditer(PATTERN_MAP["fk_alter_table"], content):
            table_name = match.group(1)
            fk_column = match.group(2)
            ref_table = match.group(3)
            ref_column = match.group(4)

            if table_name in tables:
                tables[table_name]["foreign_keys"].append(
                    {
                        "column": fk_column,
                        "references_table": ref_table,
                        "references_column": ref_column,
                    }
                )

        return tables


sql_parser = SQLparser()

tables = sql_parser.parse_sql_complete(BASEDIR / "scripts/data_model.sql")

with open(BASEDIR / "docs/tables_complete.json", "w", encoding="utf-8") as f:
    json.dump(tables, f, ensure_ascii=False, indent=2)
