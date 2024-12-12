pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/hadily/music-genre-prediction.git'
            }
        }
        stage('Build Docker Images') {
            steps {
                script {
                    bat 'docker-compose build'
                }
            }
        }
        stage('Run Containers') {
            steps {
                script {
                    bat 'docker-compose up -d'
                }
            }
        }
        // stage('Installing dependencies') {
        //     steps {
        //         script {
        //             bat 'pip install pytest librosa'
        //         }
        //     }
        // }
        // stage('Test SVM Model') {
        //     steps {
        //         script {
        //             bat 'pytest services/svm_service/test_svm_app.py'
        //         }
        //     }
        // }
        // stage('Test VGG Model') {
        //     steps {
        //         script {
        //             bat 'pytest services\vgg_service\test_vgg_app.py'
        //         }
        //     }
        // }
        stage('Stop Containers') {
            steps {
                script {
                    bat 'docker-compose down'
                }
            }
        }
    }
}
