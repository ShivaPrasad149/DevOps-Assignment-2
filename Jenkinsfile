pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-cred')
        DOCKER_IMAGE = 'shivaprasad149/devops-assignment-2-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        KUBECONFIG = credentials('kubeconfig')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/ShivaPrasad149/DevOps-Assignment-2.git'
                bat 'echo Code checked out successfully'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat """
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    // Run container for testing
                    bat "docker run -d --name test-app -p 8001:8000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    // Sleep 10 seconds
                    bat 'ping 127.0.0.1 -n 10 >nul'

                    // Health check using PowerShell curl
                    bat """
                    powershell -Command "curl http://localhost:8001/health -UseBasicParsing"
                    powershell -Command "curl http://localhost:8001/ -UseBasicParsing"
                    """

                    // Stop and remove container
                    bat "docker stop test-app && docker rm test-app"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        bat """
                        docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        """
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                        bat """
                        set KUBECONFIG=%KUBECONFIG_FILE%
                        kubectl set image deployment/devops-assignment-2-app ^
                        devops-assignment-2-app=${DOCKER_IMAGE}:${DOCKER_TAG} ^
                        --record
        
                        kubectl rollout status deployment/devops-assignment-2-app --timeout=300s
        
                        kubectl get pods -l app=devops-assignment-2-app
                        kubectl get services -l app=devops-assignment-2-app
                        """
                    }
                }
            }
        }
    }
    post {
        always {
            node('default') {
                bat 'docker system prune -f'
                bat 'echo Pipeline execution completed'
            }
        }
        success {
            node('default') {
                bat 'echo Pipeline executed successfully!'
                emailext (
                    subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                    body: "The Jenkins build ${env.BUILD_URL} completed successfully.",
                    to: "ShivaPrasad149@example.com"
                )
            }
        }
        failure {
            node('default') {
                bat 'echo Pipeline execution failed!'
                emailext (
                    subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                    body: "The Jenkins build ${env.BUILD_URL} failed. Please check the console output.",
                    to: "ShivaPrasad149@example.com"
                )
            }
        }
    }
}
