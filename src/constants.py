from pathlib import Path


BASEDIR = Path(__file__).resolve().parent.parent

PATTERN_MAP = {
    "create_ddl": r"(CREATE TABLE (?:public\.)?(\w+)\s*\(.*?\);)",
    "comment_on_table": r"COMMENT ON TABLE (?:public\.)?(\w+) IS '([^']+)'",
    "comment_on_column": r"COMMENT ON COLUMN (?:public\.)?(\w+)\.(\w+) IS '([^']+)'",
    "fk_alter_table": (
        r"ALTER TABLE ONLY (?:public\.)?(\w+)\s+ADD CONSTRAINT \w+ FOREIGN KEY \(([^)]+)\) "
        r"REFERENCES (?:public\.)?(\w+)\(([^)]+)\)"
    ),
}

EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large"

VECTOR_DB_COLLECTION_NAME = "case_3_collection"
