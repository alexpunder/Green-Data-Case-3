# error_memory.py
import hashlib
from datetime import datetime
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance


class ErrorMemory:
    """Векторная память ошибок генератора."""
    
    COLLECTION = "error_memory"
    
    def __init__(self, host="localhost", port=6333):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qdrant = QdrantClient(host=host, port=port)
        self._init_collection()
    
    def _init_collection(self):
        """Создаёт коллекцию если её нет"""
        collections = [c.name for c in self.qdrant.get_collections().collections]
        
        if self.COLLECTION not in collections:
            self.qdrant.create_collection(
                collection_name=self.COLLECTION,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"✅ Создана коллекция: {self.COLLECTION}")
    
    def add(self, task: str, sql: str, error_type: str, fix: str = None):
        """Сохраняет ошибку в память"""
        text = f"{task} [ошибка: {error_type}]"
        vector = self.model.encode(text).tolist()
        
        point_id = hashlib.md5(f"{task}{sql}{datetime.now()}".encode()).hexdigest()[:16]
        
        self.qdrant.upsert(
            self.COLLECTION,
            points=[{
                "id": point_id,
                "vector": vector,
                "payload": {
                    "task": task,
                    "sql": sql,
                    "error": error_type,
                    "fix": fix,
                    "timestamp": datetime.now().isoformat()
                }
            }]
        )
        print(f"📝 Сохранена ошибка: {error_type}")
    
    def find(self, task: str, limit: int = 3):
        """Ищет похожие ошибки из истории"""
        vector = self.model.encode(task).tolist()
        results = self.qdrant.search(self.COLLECTION, vector, limit=limit)
        
        return [
            {
                "error": r.payload["error"],
                "fix": r.payload.get("fix"),
                "similarity": r.score
            }
            for r in results
        ]
    
    def clear(self):
        """Очищает память (для тестирования)"""
        self.qdrant.delete_collection(self.COLLECTION)
        self._init_collection()
        print("🗑️ Память ошибок очищена")