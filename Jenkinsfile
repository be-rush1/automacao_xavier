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
               sh '''
                     mv BR_região_sudeste_2022.shp BR_região_sudeste_2022.shx dados_extraidos
                     rm dados_extraidos/Tmax_19610101_19801231_BR-DWGD_UFES_UTEXAS_v_3.2.3.nc
                     for x in `ls dados_extraidos | grep .nc`; do
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
