pipeline {
    agent any
    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        DOCKER_HOST = 'unix:///var/run/docker.sock'
        IMAGE_NAME = "fleet-management"
        IMAGE_TAG_BUILD = "${IMAGE_NAME}:${env.BUILD_NUMBER}-${env.GIT_BRANCH?.split('/')[-1] ?: 'main'}"
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
                MYSQL_ROOT_PASSWORD = credentials('mysql_root_password')
                MYSQL_DATABASE = credentials('db_name')
                MYSQL_USER = credentials('db_user')
                MYSQL_PASSWORD = credentials('db_password')
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
                    MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
                    MYSQL_DATABASE=${MYSQL_DATABASE}
                    MYSQL_USER=${MYSQL_USER}
                    MYSQL_PASSWORD=${MYSQL_PASSWORD}
                    DB_USER=${DB_USER}
                    DB_PASSWORD=${DB_PASSWORD}
                    DB_HOST=${DB_HOST}
                    DB_NAME=${DB_NAME}
                    IMAGE_TAG=${IMAGE_TAG_BUILD}
                    EOF
                '''
                // Detener y limpiar contenedores/redes existentes
                sh '''
                    echo "Stopping and removing existing containers..."
                    docker-compose -f docker-compose.yml down --remove-orphans
                    
                    echo "Removing old containers for this application..."
                    docker ps -a --filter "label=app=fleet-management" -q | xargs -r docker rm -f
                    
                    echo "Starting new containers with latest image..."
                    docker-compose -f docker-compose.yml up -d
                '''
                sh '''
                    echo "Waiting for application to start..."
                    sleep 30
                    echo "Verifying application status..."
                    curl -f http://localhost:5001/ || exit 1
                '''
            }
        }
        stage('Cleanup Old Images') {
            steps {
                sh '''
                    echo "Cleaning up old images (keeping last 5 builds)..."
                    docker images ${IMAGE_NAME} --format "table {{.Tag}}\t{{.ID}}" | grep -v "latest" | tail -n +6 | awk '{print $2}' | xargs -r docker rmi || true
                '''
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
            echo "Deployed image: ${IMAGE_TAG_BUILD}"
        }
        failure {
            echo 'Pipeline failed!'
            sh 'docker-compose -f docker-compose.yml logs'
        }
    }
}