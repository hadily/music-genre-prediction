pipeline {
    agent any
    //environment {
    //    DOCKER_HUB_CREDS = credentials('dockerhub') // Replace with your Jenkins credential ID
    //}
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
        //stage('Login to Docker Hub') {
            steps {
                script {
                    bat """
                    echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin
                    """
                }
            }
        //}
        //stage('Tag and Push Docker Images') {
            steps {
                script {
                    bat """
                    docker tag didi1702/frontend:latest ${DOCKER_HUB_CREDS_USR}/frontend:latest
                    docker tag didi1702/svm-flask-app:latest ${DOCKER_HUB_CREDS_USR}/svm-flask-app:latest
                    docker tag didi1702/vgg-flask-app:latest ${DOCKER_HUB_CREDS_USR}/vgg-flask-app:latest
                    """

                    bat """
                    docker push ${DOCKER_HUB_CREDS_USR}/frontend:latest
                    docker push ${DOCKER_HUB_CREDS_USR}/svm-flask-app:latest
                    docker push ${DOCKER_HUB_CREDS_USR}/vgg-flask-app:latest
                    """
                }
            }
        //}
        stage('Run Containers') {
            steps {
                script {
                    bat 'docker-compose up -d'
                }
            }
        }
        // Optionally, you can add a 'Stop Containers' stage if you need to tear down containers after running
        // stage('Stop Containers') {
        //     steps {
        //         script {
        //             bat 'docker-compose down'
        //         }
        //     }
        // }
    }
}
