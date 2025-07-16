pipeline {
    agent any
    tools{
        jdk 'jdk17'
    }
    environment{
        SCANNER_HOME=tool 'sonar-scanner'
    }

    stages {
        stage('clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('git checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/didin2003/Train-food-delivery.git'
            }
        }
        stage('Sonarqube analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=train \
                      -Dsonar.projectKey=train   -Dsonar.sources=. \
                      -Dsonar.host.url=http://51.21.235.2:9000 \
                      -Dsonar.login=sqp_96a0f95625842f026b0186e26be56146e5f3b7a6 '''
                 }
            }
        }
        stage('code quality gate') {
            steps {
                waitForQualityGate abortPipeline: false, credentialsId: 'sonar-token'
            }
        }
        stage ("Trivy File Scan") {
            steps {
                sh "trivy fs . > trivy.txt"
             }
        }
         stage ("Build Docker Image") {
            steps {
                sh "docker build -t train-food-delivery ."
            }
         }
         stage ("Tag & Push to DockerHub") {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker') {
                        sh "docker tag train-food-delivery didin8080/train-food-delivery:latest "
                        sh "docker push didin8080/train-food-delivery:latest "
                    }
                }
            }
        }
        stage ("Deploy to Container") {
             steps {
                 sh 'docker run -d --name train -p 8000:8000 didin8080/train-food-delivery:latest'
              }
        }
    }      
    post {
    always {
        emailext attachLog: true,
            subject: "'${currentBuild.result}'",
            body: """
                <html>
                <body>
                    <div style="background-color: #FFA07A; padding: 10px; margin-bottom: 10px;">
                        <p style="color: white; font-weight: bold;">Project: ${env.JOB_NAME}</p>
                    </div>
                    <div style="background-color: #90EE90; padding: 10px; margin-bottom: 10px;">
                        <p style="color: white; font-weight: bold;">Build Number: ${env.BUILD_NUMBER}</p>
                    </div>
                    <div style="background-color: #87CEEB; padding: 10px; margin-bottom: 10px;">
                        <p style="color: white; font-weight: bold;">URL: ${env.BUILD_URL}</p>
                    </div>
                </body>
                </html>
            """,
            to: 'didinpg8080@gmail.com',
            mimeType: 'text/html',
            attachmentsPattern: 'trivy.txt'
        }
    }
}    
