pipeline {
  agent any
  parameters{
    choice(name: 'Arquivos', choices: ['one', 'two', 'three'], description: '')
  }
 stages {
    stage('Instala gdown ambiente virtual') {
      steps {           
        sh 'python -m venv .venv
            . .venv/bin/activate
            pip install -r requirements.txt
            pytest -v'
      }
    }
   stage('Baixa dados xavier'){
     steps{
       sh 'cd /var/jenkins_home/.local/pipx/venvs && python3 baixa_xavier.py'
     }
   }
    stage('Deszipa dados Xavier'){
      steps{
        sh 'unzip pr_Tmax_Tmin_NetCDF_Files.zip'
      }
    }
  }
}
