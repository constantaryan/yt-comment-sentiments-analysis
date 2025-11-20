# log everything to start_docker.log
exec > /home/ubuntu/start_docker.log 2>&1

cho "Logging in to ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 254957258419.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling Docker image..."
docker pull 254957258419.dkr.ecr.ap-south-1.amazonaws.com/yt-chrome-plugin:latest

echo "Checking for existing container..."
if [ "$(docker ps -q -f name=Aryan-app)" ]; then
    echo "Stopping existing container..."
    docker stop Aryan-app
fi

if [ "$(docker ps -aq -f name=Aryan-app)" ]; then
    echo "Removing existing container..."
    docker rm Aryan-app
fi

echo "Starting new container..."
docker run -d -p 80:5000 --name Aryan-app 254957258419.dkr.ecr.ap-south-1.amazonaws.com/yt-chrome-plugin:latest

echo "Container started successfully."