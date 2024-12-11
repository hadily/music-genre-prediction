pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                // git branch: 'main', credentialsId: 'bf4702fd-31f2-4085-9abe-46eebd885777', url: 'https://github.com/hadily/music-genre-prediction.git'
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
        // stage('Upload to Docker Hub') {
        //     environment {
        //         DOCKER_HUB_CREDS = credentials('dockerhub')
        //     }
        //     steps {
        //         script {
        //             def dockerImage = "your-dockerhub-username/your-repo-name:latest"
// 
        //             // Log in to Docker Hub
        //             sh """
        //             echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin
        //             """
// 
        //             // Tag the image
        //             sh """
        //             docker tag your-local-image-name ${dockerImage}
        //             """
// 
        //             // Push the image to Docker Hub
        //             sh """
        //             docker push ${dockerImage}
        //             """
// 
        //             // Optionally log out of Docker Hub
        //             sh "docker logout"
        //         }
        //     }
        // }
        stage('Run Containers') {
            steps {
                script {
                    bat 'docker-compose up -d'
                }
            }
        }
        // stage('Run Tests') {
        //     steps {
        //         sh 'pytest tests/'
        //     }
        // }
        //stage('Stop Containers') {
        //    steps {
        //        script {
        //            bat 'docker-compose down'
        //        }
        //    }
        //}
    }
}
