from zenml import step
from typing import Dict, Any
from typing_extensions import Annotated

@step(enable_cache=False)
def fatih_terim_rag_query(
    vector_results: Dict[str, Any]
) -> Annotated[Dict[str, Any], "rag_results"]:
    """Qdrant'ta semantik arama yapar."""
    print(" RAG QUERY ÇALIŞIYOR...")

    try:
        from llm_engineering.infrastructure.db.qdrant import QdrantDatabaseConnector
        from sentence_transformers import SentenceTransformer

        qdrant = QdrantDatabaseConnector()
        model = SentenceTransformer("all-MiniLM-L6-v2")

        questions = [
            "Fatih Terim hangi takımlarda teknik direktörlük yaptı?",
            "Fatih Terim’in taktik felsefesi nedir?"
        ]

        results_all = []
        for q in questions:
            q_vec = model.encode([q])[0].tolist()
            res = qdrant.search(collection_name=vector_results["collection"], query_vector=q_vec, limit=3)
            results_all.append({
                "question": q,
                "hits": [
                    {"title": h.payload.get("title"), "score": h.score}
                    for h in res
                ]
            })
        print(f" {len(questions)} sorgu tamamlandı")
        return {"status": "ok", "queries": len(questions), "results": results_all}
    except Exception as e:
        print(f"RAG Query hata: {e}")
        return {"status": "error", "error": str(e)}
