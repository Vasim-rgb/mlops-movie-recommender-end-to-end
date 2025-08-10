pipeline {
    agent any

    environment {
        IMAGE_NAME = "shaikvasim/movie-recommender:latest"
        CONTAINER_NAME = "movie-recommender-container"
    DOCKERHUB_CREDENTIALS = "dockerhub-login" // Jenkins credentials ID
    }

    stages {
        stage('Stop Old Container') {
            steps {
                script {
                    echo "Stopping and removing old container..."
                    bat "docker stop %CONTAINER_NAME% || exit 0"
                    bat "docker rm %CONTAINER_NAME% || exit 0"
                }
            }
        }

        stage('Docker Login & Pull Image') {
            steps {
                script {
                    echo "Logging in and pulling Docker image from Docker Hub..."
                    withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
                        bat "docker pull %IMAGE_NAME%"
                    }
                }
            }
        }

        stage('Run New Container') {
            steps {
                script {
                    echo "Running new container..."
                    bat "docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%"
                }
            }
        }
    }
}