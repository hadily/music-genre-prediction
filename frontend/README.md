# build docker image
docker build -t front_app .

# run docker image
docker run -d -p 80:82 front_app