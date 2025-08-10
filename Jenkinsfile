pipeline {
    agent any
    environment {
        IMAGE_NAME = "flask-app"  // Local image name
        IMAGE_TAG  = "latest"     // Local tag
    }
    stages {
        stage('Build Docker Image') {
            steps {
                bat """
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                """
            }
        }
        stage('Stop Old Container') {
            steps {
                bat 'docker rm -f flask_app || exit 0'
            }
        }
        stage('Run New Container') {
            steps {
                bat """
                    docker run -d ^
                    --name flask_app ^
                    -p 5000:5000 ^
                    %IMAGE_NAME%:%IMAGE_TAG%
                """
            }
        }
    }
}