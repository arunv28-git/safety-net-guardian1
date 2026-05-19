pipeline {
    agent any

    environment {
        IMAGE_NAME = "kadv19/safety-net-backend:v${BUILD_NUMBER}"
        KUBECONFIG = "/var/jenkins_home/.kube/config"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/arunv28-git/safety-net-guardian1.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('backend') {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'

                    sh 'docker push $IMAGE_NAME'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {

                sh '''
                kubectl set image deployment/safety-net-backend \
                backend=$IMAGE_NAME
                '''

                sh '''
                kubectl rollout status deployment/safety-net-backend
                '''
            }
        }
    }
}
