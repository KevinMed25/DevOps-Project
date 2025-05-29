pipeline {
    agent any
    
    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        DOCKER_HOST = 'unix:///var/run/docker.sock'
        IMAGE_NAME = "fleet-management" 
        IMAGE_TAG_BUILD = "${IMAGE_NAME}:${env.BUILD_NUMBER}"
        IMAGE_TAG_LATEST = "${IMAGE_NAME}:latest"
    }

    parameters {
        booleanParam(name: 'PERFORM_DEPLOY', defaultValue: true, description: 'Check to deploy after build')
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
        
        stage('Build Docker Image') { 
            steps {
                sh "docker build -t ${IMAGE_TAG_BUILD} ."
                sh "docker tag ${IMAGE_TAG_BUILD} ${IMAGE_TAG_LATEST}"
            }
        }
        
        stage('Deploy') {
            when {
                expression { params.PERFORM_DEPLOY == true }
            }
            environment {
                DB_USER = credentials('db_user')
                DB_PASSWORD = credentials('db_password')
                DB_HOST = credentials('db_host')
                DB_NAME = credentials('db_name')
                APP_ENV = "development" 
            }
            steps {
                sh '''
                    echo "Creating .env file for deployment..."
                    cat > .env << EOF
                    ENV=${APP_ENV}
                    DB_USER=${DB_USER}
                    DB_PASSWORD=${DB_PASSWORD}
                    DB_HOST=${DB_HOST}
                    DB_NAME=${DB_NAME}
                    IMAGE_TAG=${IMAGE_TAG_LATEST} 
                    EOF
                '''
                sh '''
                    docker-compose down
                    docker-compose up -d
                '''
                sh '''
                    echo "Waiting for application to start..."
                    sleep 15 
                    echo "Verifying application status..."
                    curl -f http://localhost:5001/ || exit 1 
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs() 
                sh "docker rmi ${IMAGE_TAG_BUILD} || true" 
            }
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
            script {
                sh 'docker-compose logs'
            }
        }
    }
}