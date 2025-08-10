pipeline {
    agent any

    environment {
        IMAGE_NAME = "myimage:latest"       // Change this
        CONTAINER_NAME = "mycontainer"      // Change this
        DOCKERHUB_CREDENTIALS = "dockerhub-creds" // Jenkins credentials ID
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    bat "docker build -t %IMAGE_NAME% ."
                }
            }
        }

        stage('Stop Old Container') {
            steps {
                script {
                    echo "Stopping and removing old container..."
                    bat "docker stop %CONTAINER_NAME% || exit 0"
                    bat "docker rm %CONTAINER_NAME% || exit 0"
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

        stage('Push to Docker Hub') {
            when {
                expression { return false } // Change to true if you want to push
            }
            steps {
                script {
                    echo "Pushing image to Docker Hub..."
                    withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
                        bat "docker tag %IMAGE_NAME% %DOCKER_USER%/%IMAGE_NAME%"
                        bat "docker push %DOCKER_USER%/%IMAGE_NAME%"
                    }
                }
            }
        }
    }
}