PATTERN_MAP = {
    "create_ddl": r"(CREATE TABLE (?:public\.)?(\w+)\s*\(.*?\);)",
    "comment_on_table": r"COMMENT ON TABLE (?:public\.)?(\w+) IS '([^']+)'",
    "comment_on_column": r"COMMENT ON COLUMN (?:public\.)?(\w+)\.(\w+) IS '([^']+)'",
    "fk_alter_table": (
        r"ALTER TABLE ONLY (?:public\.)?(\w+)\s+ADD CONSTRAINT \w+ FOREIGN KEY \(([^)]+)\) "
        r"REFERENCES (?:public\.)?(\w+)\(([^)]+)\)"
    ),
}
