# build docker image
docker build -t svm_flask_app .

# run docker image
docker run -d -p 5000:5000 svm_flask_app
