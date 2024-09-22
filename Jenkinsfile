pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                // Criar o ambiente virtual e instalar o gdown (caso ainda não tenha sido criado)
                sh '''
                if [ ! -d "venv" ]; then
                    python3 -m venv venv
                    ./venv/bin/pip install gdown
                fi
                '''
            }
        }

        stage('Run Python Script') {
            steps {
                // Ativar o ambiente virtual e rodar o script Python que usa o gdown
                sh '''
                source ./venv/bin/activate
                python3 baixa_xavier.py
                '''
            }
        }
    }

    post {
        always {
            // Clean up if necessary
            sh 'deactivate || true'
        }
    }
}
