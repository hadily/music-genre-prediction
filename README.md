# Music Genre Prediction

### Build the services
docker-compose build

### Run the containers
docker-compose up

### Pull the Jenkins Docker image
docker pull jenkins/jenkins:lts

### Run Jenkins as a container
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins --restart=always jenkins/jenkins:lts

Access Jenkins through your browser at http://localhost:8080

### Retrieve the Jenkins unlock key from the Docker container logs
docker logs jenkins
