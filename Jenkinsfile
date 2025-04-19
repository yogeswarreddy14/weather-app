pipeline {
    agent any

    environment {
        DOCKER_HOST = 'tcp://localhost:2375'
    }

    stages {
        stage('Check Docker Status') {
            steps {
                script {
                    try {
                        bat 'docker info'
                    } catch (Exception e) {
                        error "Docker is not running or not properly configured. Please ensure Docker Desktop is running and configured correctly."
                    }
                }
            }
        }

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/yogeswarreddy14/weather-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        bat 'docker build -t weather-app .'
                    } catch (Exception e) {
                        error "Failed to build Docker image: ${e.message}"
                    }
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    try {
                        bat 'docker stop weather-container || exit 0'
                        bat 'docker rm weather-container || exit 0'
                        bat 'docker run -d -p 8000:8000 --name weather-container weather-app'
                    } catch (Exception e) {
                        error "Failed to run container: ${e.message}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed'
        }
        failure {
            echo 'Pipeline failed'
        }
        success {
            echo 'Pipeline succeeded'
        }
    }
}
