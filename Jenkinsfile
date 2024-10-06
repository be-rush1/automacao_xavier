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
                    pwd
                    ls
                   '''
            }
        }
        stage('Deszipa arquivo'){
            steps{
                sh 'pwd'
            }
        }
       stage('Corta Dados'){
           steps{
               sh '''for x in `ls /dados_extraidos | grep .nc`; do
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
