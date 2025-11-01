from zenml import step
from datetime import datetime
from typing import List, Dict, Any
from typing_extensions import Annotated
import time

@step(enable_cache=False)
def fatih_terim_ddg_crawler(mode: str = "real") -> Annotated[List[Dict[str, Any]], "search_results"]:
    """Fatih Terim verisini DuckDuckGo'dan çeker veya test datası döndürür."""
    print(" CRAWLER ÇALIŞIYOR...")

    if mode == "test":
        return _create_test_data()

    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS()
        queries = ["Fatih Terim", "Fatih Terim Galatasaray", "Fatih Terim milli takım"]
        all_results = []

        for q in queries:
            time.sleep(2)
            results = list(ddgs.text(keywords=q, max_results=5))
            for r in results:
                all_results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", ""),
                    "content": f"{r.get('title','')}. {r.get('body','')}",
                    "query": q,
                    "timestamp": datetime.now().isoformat()
                })
        return all_results
    except Exception as e:
        print(f"DDG hata: {e}")
        return _create_test_data()

def _create_test_data() -> List[Dict[str, Any]]:
    test = []
    topics = [
        "Galatasaray başarıları", "Milli takım kariyeri",
        "İtalya deneyimi", "Taktik felsefesi", "Disiplin anlayışı"
    ]
    for i, t in enumerate(topics):
        test.append({
            "title": f"Fatih Terim {t}",
            "snippet": f"Fatih Terim’in {t} üzerine detaylı bilgi.",
            "url": f"https://example.com/{i}",
            "content": f"Fatih Terim’in {t} hakkında önemli detaylar.",
            "query": "Fatih Terim",
            "timestamp": datetime.now().isoformat()
        })
    print(f" Test verisi oluşturuldu: {len(test)} kayıt")
    return test
