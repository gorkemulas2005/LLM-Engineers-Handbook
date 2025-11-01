from zenml import step
import mlflow
from typing import Any
from typing_extensions import Annotated

@step(enable_cache=False)
def automm_model_trainer(train_data) -> Annotated[Any, "trained_model"]:
    """AutoGluon Multimodal AutoML model eğitimi"""
    print(" STEP 2: MODEL TRAINER ÇALIŞIYOR...")

    try:
        from autogluon.multimodal import MultiModalPredictor
        print(" AutoGluon yüklü, model başlatılıyor...")
    except ImportError:
        print(" AutoGluon kurulu değil! Poetry'de kurmak için:")
        print(" poetry add autogluon.multimodal==1.1.1")
        return None

    mlflow.set_experiment("autogluon_multimodal_experiment")

    with mlflow.start_run(run_name="automm_train_run"):
        mlflow.log_param("model_type", "AutoGluon_MultiModal")
        mlflow.log_param("problem_type", "binary")

        predictor = MultiModalPredictor(label="label", problem_type="binary")

        print(" Model eğitimi başlatılıyor...")
        predictor.fit(
            train_data=train_data,
            time_limit=60,  # küçük veri için hızlı deneme
            presets="medium_quality"
        )

        mlflow.log_metric("train_samples", len(train_data))
        mlflow.set_tag("project", "multimodal_automl_demo")

        print(" Model eğitim tamamlandı, MLflow'a kaydediliyor...")
        predictor.save("automm_model")
        mlflow.log_artifacts("automm_model")

        print(" MODEL EĞİTİMİ TAMAMLANDI ")
        return predictor
