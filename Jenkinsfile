pipeline {
    agent any

    environment {
        IMAGE_NAME = "safety-net-backend:v3"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'cd backend && docker build -t $IMAGE_NAME .'
            }
        }

        stage('Build Success') {
            steps {
                echo 'Docker image built successfully.'
            }
        }
    }
}