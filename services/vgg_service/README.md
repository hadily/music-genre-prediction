### build docker image
docker build -t vgg_flask_app .

### run docker image
docker run -d -p 5001:5001 vgg_flask_app