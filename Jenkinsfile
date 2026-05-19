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

        stage('Load Image into Minikube') {
            steps {
                sh 'minikube image load $IMAGE_NAME'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/backend-deployment.yaml'
                sh 'kubectl apply -f k8s/backend-service.yaml'
            }
        }

        stage('Check Pods') {
            steps {
                sh 'kubectl get pods'
            }
        }
    }
}