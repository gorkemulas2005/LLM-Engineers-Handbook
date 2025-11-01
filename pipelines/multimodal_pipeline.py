from zenml import pipeline
from steps.multimodal.data_loader import multimodal_data_loader
from steps.multimodal.model_trainer import automm_model_trainer
from steps.multimodal.model_evaluator import automm_model_evaluator

@pipeline(enable_cache=False)
def multimodal_pipeline():
    """AutoGluon AutoML Multimodal Pipeline"""
    print("=" * 70)
    print(" AUTOGLUON AUTOMM PIPELINE BAŞLATILDI ")
    print(" DATA → TRAIN → EVAL → MLFLOW")
    print("=" * 70)

    train_data, test_data = multimodal_data_loader()
    model = automm_model_trainer(train_data)
    automm_model_evaluator(model, test_data)

    print("=" * 70)
    print(" PIPELINE TAMAMLANDI ")
    print(" MLflow UI: http://localhost:5000")
    print("=" * 70)

if __name__ == "__main__":
    multimodal_pipeline()
