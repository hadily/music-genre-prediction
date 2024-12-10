pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', credentialsId: 'bf4702fd-31f2-4085-9abe-46eebd885777', url: 'https://github.com/hadily/music-genre-prediction.git'
            }
        }
        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }
        stage('Run Containers') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }
        stage('Stop Containers') {
            steps {
                script {
                    sh 'docker-compose down'
                }
            }
        }
    }
}
