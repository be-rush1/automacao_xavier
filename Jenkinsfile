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
                    mkdir data/extracted_data
                fi
                '''
            }
        }

        stage('Baixa Dados do Xavier') {
            steps {
                // Ativar o ambiente virtual e rodar o script Python que usa o gdown
                sh '''
                . ./venv/bin/activate
                python3 baixa_xavier.py
                '''
            }
        }
        stage('Deszipa arquivo'){
            steps{
                sh 'unzip -o data/seu_arquivo.zip -d data/extracted_data/'
            }
        }
       stage('Corta Dados'){
           steps{
               sh '''for x in data/extracted_data; do
                     python3 corta_dados.py $x
                     done
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
