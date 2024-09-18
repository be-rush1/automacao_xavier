pipeline {
  agent any
  parameters{
    choice(name: 'Arquivos', choices: ['one', 'two', 'three'], description: '') }
}
 stages {
    stage('Deszipando dados zipados do Xavier') {
      steps {           
        sh 'unzip pr_Tmax_Tmin_NetCDF_Files.zip'
      }
    }
    stage('Corta os Dados') {
      steps {
         sh 'python3 corta_dados.py'
      }
    }
  }
}
