pipeline {
  agent any
  parameters{
    choice(name: 'Arquivos', choices: ['one', 'two', 'three'], description: '')
  }
 stages {
    stage('Instala gdown ambiente virtual') {
      steps {           
        sh ''' python3 -m venv .venv
            source ./venv/bin/activate
            pip install gdown
            python3 baixa_xavier.py
            '''
      }
    }
    stage('Deszipa dados Xavier'){
      steps{
        sh 'unzip pr_Tmax_Tmin_NetCDF_Files.zip'
      }
    }
  }
}
