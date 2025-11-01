pipeline {
    agent any

    environment {
        MLFLOW_RUN_NAME = "jenkins_build_${BUILD_NUMBER}"
    }

    stages {
        stage('Setup Poetry Env') {
            steps {
                bat '''
                echo Setting up Poetry environment...
                cd C:\\Users\\gorke\\LLM-Engineers-Handbook
                poetry env use 3.11
                poetry install
                '''
            }
        }

        stage('Start Docker') {
            steps {
                bat '''
                echo Starting Docker containers...
                cd C:\\Users\\gorke\\LLM-Engineers-Handbook
                docker compose up -d
                timeout /t 15
                '''
            }
        }

        stage('Run ZenML Pipeline') {
            steps {
                bat '''
                echo Running Fatih Terim RAG pipeline...
                cd C:\\Users\\gorke\\LLM-Engineers-Handbook
                poetry run python pipelines/fatih_terim_pipeline.py
                '''
            }
        }

        stage('Track with MLflow') {
            steps {
                bat '''
                echo Launching MLflow UI...
                cd C:\\Users\\gorke\\LLM-Engineers-Handbook
                poetry run mlflow ui --port 5000
                '''
            }
        }
    }

    post {
        always {
            bat '''
            echo Shutting down Docker containers...
            cd C:\\Users\\gorke\\LLM-Engineers-Handbook
            docker compose down
            '''
        }
    }
}
