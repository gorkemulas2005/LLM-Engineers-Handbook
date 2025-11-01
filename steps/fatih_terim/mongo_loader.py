from zenml import step
from typing import List, Dict, Any
from typing_extensions import Annotated

@step(enable_cache=False)
def fatih_terim_mongo_loader(
    search_results: List[Dict[str, Any]]
) -> Annotated[Dict[str, Any], "mongo_results"]:
    """Crawler verisini MongoDB’ye kaydeder."""
    print(" MONGO LOADER ÇALIŞIYOR...")

    try:
        from llm_engineering.domain.documents import ArticleDocument, UserDocument

        user = UserDocument(first_name="Fatih", last_name="TerimCrawler", full_name="Fatih_Terim_Crawler")
        user.save()

        count = 0
        for d in search_results:
            art = ArticleDocument(
                content={"title": d["title"], "content": d["content"], "snippet": d["snippet"]},
                platform="web_crawl",
                author_full_name="Fatih_Terim_Crawler",
                author_id=user.id,
                link=d["url"],
                metadata={"query": d["query"], "timestamp": d["timestamp"]}
            )
            art.save()
            count += 1

        print(f" {count} kayıt MongoDB’ye yazıldı")
        return {"status": "ok", "count": count}
    except Exception as e:
        print(f"MongoDB hata: {e}")
        return {"status": "error", "error": str(e)}
