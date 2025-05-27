pipeline {
    agent any
    
    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verificación Docker') {
            steps {
                sh '''
                    echo "USUARIO: $(whoami)"
                    echo "PATH: $PATH"
                    which docker || echo "docker NO está disponible"
                    docker version || echo "docker NO funciona"
                '''
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
            script {
                sh 'docker rmi fleet-app-lint || true'
            }
        }
    }
}
