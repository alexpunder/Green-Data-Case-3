import json

from qdrant_client import QdrantClient, models

from constants import VECTOR_DB_COLLECTION_NAME, EMBEDDING_MODEL_NAME, BASEDIR

client = QdrantClient(url="http://localhost:6333")

# client.delete_collection(collection_name=VECTOR_DB_COLLECTION_NAME)

# collections = client.get_collections().collections
# exists = any(c.name == VECTOR_DB_COLLECTION_NAME for c in collections)

# if not exists:
#     client.create_collection(
#         collection_name=VECTOR_DB_COLLECTION_NAME,
#         vectors_config=models.VectorParams(
#             size=client.get_embedding_size(EMBEDDING_MODEL_NAME),
#             distance=models.Distance.COSINE
#         )
#     )
#     print(f"Создана коллекция: {VECTOR_DB_COLLECTION_NAME}")
# else:
#     print(f"Коллекция уже существует: {VECTOR_DB_COLLECTION_NAME}")


# with open(BASEDIR / "docs/tables_complete.json", "r", encoding="utf-8") as f:
#     tables = json.load(f)

# documents = []
# payloads = []
# ids = []
# for idx, (table_name, table_info) in enumerate(tables.items()):
#     search_text = f"Таблица {table_name}"
    
#     if table_info.get("description"):
#         search_text += f": {table_info["description"]}"
    
#     columns = list(table_info.get("column_comments", {}).items())
#     if columns:
#         search_text += ". Поля: "
#         search_text += ", ".join([f"{col} ({comment})" for col, comment in columns])
    
#     if table_info.get("foreign_keys"):
#         fk_desc = []
#         for fk in table_info["foreign_keys"]:
#             fk_desc.append(f"{fk["column"]} → {fk["references_table"]}.{fk["references_column"]}")
#         if fk_desc:
#             search_text += ". Связан с: " + ", ".join(fk_desc)
    
#     documents.append(models.Document(text=search_text, model=EMBEDDING_MODEL_NAME))
#     payloads.append({
#         "table_name": table_name,
#         "description": table_info.get("description", ""),
#         "columns_count": len(table_info.get("column_comments", {})),
#         "fk_count": len(table_info.get("foreign_keys", [])),
#         "create_table_sql": table_info.get("create_table_sql", "")
#     })
#     ids.append(idx)


# client.upload_collection(
#     collection_name=VECTOR_DB_COLLECTION_NAME,
#     vectors=documents,
#     ids=ids,
#     payload=payloads,
# )

# print(f"Загружено {len(documents)} таблиц в Qdrant")

# count = client.count(collection_name=VECTOR_DB_COLLECTION_NAME)
# print(f"Всего точек в коллекции: {count.count}")

def search_tables(query: str, top_k: int = 5):
    """Ищет таблицы, релевантные запросу"""
    
    search_result = client.query_points(
        collection_name=VECTOR_DB_COLLECTION_NAME,
        query=models.Document(text=query, model=EMBEDDING_MODEL_NAME),
        limit=top_k,
    ).points

    results = []
    for point in search_result:
        results.append({
            "table_name": point.payload["table_name"],
            "description": point.payload["description"],
            "score": point.score,
            "create_table_sql": point.payload["create_table_sql"]
        })
    
    return results
