pipeline {
  agent any
  parameters{
    choice(name: 'Arquivos', choices: ['one', 'two', 'three'], description: '')
  }
 stages {
    stage('Baixa dados do Xavier') {
      steps {           
        sh 'pip install gdown'
      }
    }
    stage('Deszipa dados Xavier'){
      steps{
        sh 'unzip pr_Tmax_Tmin_NetCDF_Files.zip'
      }
    }
  }
}
