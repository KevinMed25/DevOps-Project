pipeline {
    agent any

    parameters {
        booleanParam(name: 'PERFORM_DEPLOY', defaultValue: true, description: 'Check to build and deploy. Uncheck to only build.')
    }

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        IMAGE_NAME = "fleet-management"
        IMAGE_TAG_LATEST = "${IMAGE_NAME}:latest"
        DOCKER_HOST = 'unix:///var/run/docker.sock' 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_TAG_LATEST}"
                sh "docker build -t ${IMAGE_TAG_LATEST} ."
                echo "Docker image ${IMAGE_TAG_LATEST} built. Listing images:"
                sh "docker images | grep ${IMAGE_NAME} || true"
            }
        }

        stage('Deploy Application') {
            when {
                expression { params.PERFORM_DEPLOY == true }
            }
            steps {
                echo "Deploying application..."
                sh "docker-compose -f docker-compose.yml down --remove-orphans"
                sh "docker-compose -f docker-compose.yml up -d --build"
                echo "Deployment attempted. Waiting briefly for services to start..."
                sh "sleep 10"
                echo "Current Docker containers:"
                sh "docker ps -a | grep ${IMAGE_NAME} || true"
                echo "Logs from 'app' container (if running):"
                sh "docker-compose -f docker-compose.yml logs app || true"
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Cleaning workspace."
            cleanWs()
        }
    }
}