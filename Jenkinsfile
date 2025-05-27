pipeline {
    agent {
        docker {
            image 'bretfisher/jenkins-docker-client:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock --privileged'
            reuseNode true  
        }
    }
    
    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
        PATH = "/usr/local/bin:$PATH:/usr/bin:/bin:/usr/sbin:/sbin"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Linting') {
            steps {
                script {
                    sh 'docker build -t fleet-app-lint -f Dockerfile.lint .'
                    sh 'docker run --rm fleet-app-lint'
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                sh script: '/bin/sh -c "docker build -t fleet-management ."', returnStdout: true
            }
        }
        
        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'development'
                }
            }
            environment {
                DB_USER = credentials('db_user')
                DB_PASSWORD = credentials('db_password')
                DB_HOST = credentials('db_host')
                DB_NAME = credentials('db_name')
                JWT_SECRET_KEY = credentials('jwt_secret_key')
                ENV = "${BRANCH_NAME == 'main' ? 'PRODUCTION' : 'DEVELOPMENT'}"
            }
            steps {
                sh '''
                    docker-compose down
                    docker-compose up -d
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
            sh 'docker rmi fleet-app-lint || true'
        }
    }
}
environment {
    PATH = "${PATH}:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
}