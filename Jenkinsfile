pipeline {
    agent {
        docker {
            image 'docker:dind'  
            args '--privileged -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        DOCKER_COMPOSE_VERSION = '2.0'
        DOCKER_HOST = 'unix:///var/run/docker.sock'  
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Docker Compose') {
            steps {
                sh '''
                    apk add --no-cache py3-pip
                    pip3 install docker-compose
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
                script {
                    sh 'docker-compose build'
                }
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
            script {
                sh 'docker image inspect fleet-app-lint &>/dev/null && docker rmi fleet-app-lint || true'
            }
        }
    }
}