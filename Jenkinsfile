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

        stage('Baixa Dados do Xavier') {
            steps {
                // Ativar o ambiente virtual e rodar o script Python que usa o gdown
                sh '''
                   https://drive.google.com/file/d/11yTPRMF9RgyF4irAWWydm8IKzlr3eI8_/view?usp=drive_link
                   . ./venv/bin/activate
                   python3 baixa_xavier.py
                   '''
            }
        }
        stage('Deszipa arquivo'){
            steps{
                sh '''
                   unzip -o pr_Tmax_Tmin_NetCDF_Files.zip 'pr_*' -d dados_extraidos/
                   '''
            }
        }
       stage('Corta Dados'){
           steps{
               sh '''
                     mv BR_região_sudeste_2022.shp BR_região_sudeste_2022.shx dados_extraidos
                     for x in `ls dados_extraidos | grep .nc`; do
                     python3 corta_dados.py $x
                     done
                  '''
           }
       }
    }
}
