from zenml import step
import mlflow
import numpy as np
from typing import Any
from typing_extensions import Annotated

@step(enable_cache=False)
def automm_model_evaluator(model: Any, test_data) -> Annotated[float, "accuracy"]:
    """Modeli test et ve sonucu MLflow'a yükle"""
    print(" STEP 3: MODEL EVALUATOR ÇALIŞIYOR...")

    if model is None:
        print(" Model yok, değerlendirme atlandı.")
        return 0.0

    predictions = model.predict(test_data)
    labels = test_data['label'].to_numpy()
    accuracy = float(np.mean(predictions == labels))

    with mlflow.start_run(run_name="automm_eval_run"):
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("test_samples", len(test_data))
        mlflow.set_tag("evaluation", "true")
        mlflow.set_tag("pipeline", "multimodal_automl")

    print(f" Model doğruluk oranı: {accuracy:.3f}")
    print(" Sonuç MLflow'a loglandı ✅")
    return accuracy
