from zenml import pipeline
from steps.fatih_terim import (
    fatih_terim_ddg_crawler,
    fatih_terim_mongo_loader,
    fatih_terim_vectorizer,
    fatih_terim_rag_query,
    fatih_terim_mlflow_tracker,
)

@pipeline(enable_cache=False)
def fatih_terim_pipeline(mode: str = "real"):
    """Tam entegre Fatih Terim RAG pipeline"""
    print("=" * 60)
    print(" FATİH TERİM RAG PIPELINE BAŞLADI")
    print("=" * 60)

    results = fatih_terim_ddg_crawler(mode=mode)
    mongo_out = fatih_terim_mongo_loader(results)
    vectors = fatih_terim_vectorizer(results)
    rag_out = fatih_terim_rag_query(vectors)
    fatih_terim_mlflow_tracker(rag_out)

    print("=" * 60)
    print(" FATİH TERİM RAG PIPELINE TAMAMLANDI ")
    print("=" * 60)

if __name__ == "__main__":
    fatih_terim_pipeline(mode="test")  # test moduyla başlat
