pipeline {
    agent any

    environment {
        APP_NAME = "movie-recommender"
        IMAGE_NAME = "movie-recommender:latest"
        CONTAINER_NAME = "movie-recommender-container"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/Vasim-rgb/mlops-movie-recommender-end-to-end.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Stop Old Container') {
            steps {
                echo "Stopping old container if exists..."
                sh '''
                if [ $(docker ps -q -f name=${CONTAINER_NAME}) ]; then
                    docker stop ${CONTAINER_NAME}
                    docker rm ${CONTAINER_NAME}
                fi
                '''
            }
        }

        stage('Run New Container') {
            steps {
                echo "Running new container..."
                sh 'docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}'
            }
        }
    }

    post {
        success {
            echo "Application deployed successfully on http://localhost:5000"
        }
        failure {
            echo " Build failed! Check logs."
        }
    }
}