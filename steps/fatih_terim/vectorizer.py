from zenml import step
from datetime import datetime
from typing import List, Dict, Any
from typing_extensions import Annotated

@step(enable_cache=False)
def fatih_terim_vectorizer(
    articles: List[Dict[str, Any]]
) -> Annotated[Dict[str, Any], "vector_results"]:
    """Metinleri embedding’e dönüştürüp Qdrant’a yazar."""
    print(" VECTORIZER ÇALIŞIYOR...")

    try:
        from llm_engineering.infrastructure.db.qdrant import QdrantDatabaseConnector
        from sentence_transformers import SentenceTransformer
        from qdrant_client.http import models

        model = SentenceTransformer("all-MiniLM-L6-v2")
        texts = [a["content"] for a in articles]
        embeddings = model.encode(texts)

        qdrant = QdrantDatabaseConnector()
        coll = "fatih_terim_articles"
        qdrant.recreate_collection(
            collection_name=coll,
            vectors_config=models.VectorParams(size=len(embeddings[0]), distance=models.Distance.COSINE)
        )

        points = []
        for i, (text, vec) in enumerate(zip(texts, embeddings)):
            points.append({
                "id": i,
                "vector": vec.tolist(),
                "payload": {
                    "text": text,
                    "title": articles[i]["title"],
                    "source": "fatih_terim_pipeline",
                    "timestamp": datetime.now().isoformat()
                }
            })

        qdrant.upsert(collection_name=coll, points=points)
        print(f" {len(points)} vektör Qdrant’a kaydedildi")
        return {"collection": coll, "count": len(points), "status": "ok"}
    except Exception as e:
        print(f"Vectorizer hata: {e}")
        return {"status": "error", "error": str(e)}
