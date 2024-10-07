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
                   . ./venv/bin/activate
                   #python3 baixa_xavier.py
                   ls
                   '''
            }
        }
        stage('Deszipa arquivo'){
            steps{
                sh '''
                   #unzip -o pr_Tmax_Tmin_NetCDF_Files.zip 'pr_*' -d dados_extraidos/
                   #rm pr_Tmax_Tmin_NetCDF_Files.zip
                   python3 descomp.py pr.npz
                   python3 converte.py 
                   ls
                   '''
            }
        }
       stage('Corta Dados'){
           steps{
               sh '''
                     python3 corta_dados.py data.nc
                  '''
           }
       }
    }
}
