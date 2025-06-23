pipeline {
    agent any
    stages {
        stage('Install dependencies') {
            steps {
                // Criar o ambiente virtual e instalar o gdown (caso ainda não tenha sido criado)
                sh '''
                if [ ! -d "venv" ]; then
                    python3 -m venv venv
                fi
                ./venv/bin/pip install gdown
                ./venv/bin/pip install rioxarray
                '''
            }
        }

        stage('Baixa Dados do Xavier') {
            steps {
                // Ativar o ambiente virtual e rodar o script Python que usa o gdown
                sh '''
                   . ./venv/bin/activate
                   python3 baixa_xavier.py
                   ls
                   '''
            }
        }
        stage('Deszipa arquivo'){
            steps{
                sh '''
                   unzip -o pr_Tmax_Tmin_NetCDF_Files.zip 'pr_*' -d dados_extraidos/
                   rm pr_Tmax_Tmin_NetCDF_Files.zip
                   '''
            }
        }
       stage('Faz Média Mensal dos Dados'){
           steps{
               sh '''

                  for x in `ls dados_extraidos | grep .nc`; do
                     touch media_$x
                     cdo monmean dados_extraidos/$x media_$x
                  done
                  '''
           }
       }
       stage('Corta Dados'){
           steps{
               sh ''' 
                    . ./venv/bin/activate
                    for x in `ls | grep media`; do
                         python3 corta_dados.py $x
                    done
                  '''
           }
       }
       stage('Calcula Anomalia, Normaliza e Remove tendência'){
            steps{
                sh '''
                    . ./venv/bin/activate
                    python3 novo.py

                '''
            }
        }
    }
}
