import re
import json

from constants import PATTERN_MAP

def parse_sql_complete(sql_file_path):
    """Извлекает COMMENT ON TABLE, COMMENT ON COLUMN и FOREIGN KEY из SQL-дампа"""
    
    with open(sql_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    tables = {}
    
    for match in re.finditer(PATTERN_MAP["create_ddl"], content, re.DOTALL):
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
        clean_comment = comment.split(',')[0].strip()
        
        if table_name in tables:
            tables[table_name]["description"] = clean_comment
    
    for match in re.finditer(PATTERN_MAP["comment_on_column"], content):
        table_name = match.group(1)
        column_name = match.group(2)
        comment = match.group(3)
        clean_comment = comment.split(",")[0].strip()
        
        if table_name in tables:
            tables[table_name]["column_comments"][column_name] = clean_comment
    
    for match in re.finditer(PATTERN_MAP["fk_alter_table"], content):
        table_name = match.group(1)
        fk_column = match.group(2)
        ref_table = match.group(3)
        ref_column = match.group(4)
        
        if table_name in tables:
            tables[table_name]["foreign_keys"].append({
                "column": fk_column,
                "references_table": ref_table,
                "references_column": ref_column
            })
    
    return tables

tables = parse_sql_complete("scripts/data_model.sql")

with open("docs/tables_complete.json", "w", encoding="utf-8") as f:
    json.dump(tables, f, ensure_ascii=False, indent=2)
