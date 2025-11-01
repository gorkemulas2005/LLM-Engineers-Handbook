from zenml import step
from typing import Dict, Any
from typing_extensions import Annotated
from datetime import datetime
import mlflow

@step(enable_cache=False)
def fatih_terim_mlflow_tracker(
    rag_results: Dict[str, Any]
) -> Annotated[Dict[str, Any], "mlflow_results"]:
    """Pipeline sonuçlarını MLflow'a loglar."""
    print(" MLFLOW TRACKER ÇALIŞIYOR...")

    try:
        mlflow.set_experiment("fatih_terim_pipeline")
        with mlflow.start_run(run_name="fatih_terim_rag"):
            mlflow.log_param("pipeline", "Fatih_Terim_RAG")
            mlflow.log_param("timestamp", datetime.now().isoformat())
            mlflow.log_metric("queries", rag_results.get("queries", 0))
            mlflow.log_metric("success", 1 if rag_results.get("status") == "ok" else 0)
            mlflow.set_tag("rag", "true")
            mlflow.set_tag("zenml", "integrated")
        print(" MLflow log tamamlandı")
        return {"status": "ok"}
    except Exception as e:
        print(f"MLflow hata: {e}")
        return {"status": "error", "error": str(e)}
