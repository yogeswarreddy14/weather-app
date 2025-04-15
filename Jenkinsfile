pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/yogeswarreddy14/weather-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t weather-app .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker stop weather-container || exit 0'
                bat 'docker rm weather-container || exit 0'
                bat 'docker run -d -p 8000:8000 --name weather-container weather-app'
            }
        }
    }
}
