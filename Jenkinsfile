pipeline {
    agent any

    environment {
        // Python & proje dizini
        PROJECT_DIR = "C:\\Users\\gorke\\LLM-Engineers-Handbook"
        POETRY_EXE  = "C:\\Users\\gorke\\AppData\\Roaming\\Python\\Scripts\\poetry.exe"
    }

    stages {

        stage('Setup Poetry Env') {
            steps {
                bat '''
                echo Setting up Poetry environment...
                cd %PROJECT_DIR%
                "%POETRY_EXE%" env use 3.11
                "%POETRY_EXE%" install
                '''
            }
        }

        stage('Start Docker') {
            steps {
                bat '''
                echo Starting Docker containers...
                cd %PROJECT_DIR%
                docker compose up -d
                '''
            }
        }

        stage('Run ZenML Pipeline') {
            steps {
                bat '''
                echo Running Fatih Terim Pipeline via ZenML...
                cd %PROJECT_DIR%
                "%POETRY_EXE%" run python pipelines/fatih_terim_pipeline.py
                '''
            }
        }

        stage('Track with MLflow') {
            steps {
                bat '''
                echo Opening MLflow UI on port 5000...
                cd %PROJECT_DIR%
                start "" "%POETRY_EXE%" run mlflow ui --port 5000
                '''
            }
        }
    }

    post {
        always {
            bat '''
            echo Shutting down Docker containers...
            cd %PROJECT_DIR%
            docker compose down
            '''
        }
    }
}
