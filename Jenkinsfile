pipeline {
  agent any

  environment {
    POETRY = 'C:\\Users\\gorke\\AppData\\Roaming\\Python\\Scripts\\poetry.exe'
    PY311  = 'C:\\Program Files\\Python311\\python.exe'
    PROJ   = 'C:\\Users\\gorke\\LLM-Engineers-Handbook'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Poetry Setup') {
      steps {
        bat '''
        cd "%PROJ%"
        echo === Ensure Poetry points to Python 3.11 ===
        "%POETRY%" env use "%PY311%"
        echo === Install project deps (idempotent) ===
        "%POETRY%" install --no-interaction --no-ansi
        echo === Sanity check: all imports ===
        "%POETRY%" run python -c "import zenml, mlflow, pymongo, qdrant_client, sentence_transformers; print('OK_IMPORTS')"
        '''
      }
    }

    stage('Start Docker') {
      steps {
        bat '''
        cd "%PROJ%"
        docker compose up -d
        '''
      }
    }

    stage('Run ZenML Pipeline') {
      steps {
        bat '''
        cd "%PROJ%"
        "%POETRY%" run python -m pipelines.fatih_terim_pipeline
        '''
      }
    }

    stage('Track with MLflow (optional)') {
      when { expression { return false } } // istersen true yap
      steps {
        bat '''
        cd "%PROJ%"
        start "" "%POETRY%" run mlflow ui --port 5000
        '''
      }
    }
  }

  post {
    always {
      bat '''
      cd "%PROJ%"
      docker compose down
      '''
    }
  }
}
