#!/bin/bash
exec > /home/ubuntu/start_docker.log 2>&1

echo "Logging in to ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 590716168581.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling Docker image..."
docker pull 590716168581.dkr.ecr.ap-south-1.amazonaws.com/yt_comments_sentiments_analysis:latest

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
# docker run -d -p 80:5000 --name Aryan-app --restart unless-stopped 590716168581.dkr.ecr.ap-south-1.amazonaws.com/yt_comments_sentiments_analysis:latest
DAGSHUB_USERNAME=$(aws ssm get-parameter --name "/dagshub/constantaryan/username" --query "Parameter.Value" --output text --region ap-south-1)
DAGSHUB_TOKEN=$(aws ssm get-parameter --name "/dagshub/constantaryan/token" --with-decryption --query "Parameter.Value" --output text --region ap-south-1)

docker run -d \
-p 80:5000 \
--name Aryan-app \
--restart unless-stopped \
-e DAGSHUB_USERNAME="$DAGSHUB_USERNAME" \
-e DAGSHUB_TOKEN="$DAGSHUB_TOKEN" \
590716168581.dkr.ecr.ap-south-1.amazonaws.com/yt_comments_sentiments_analysis:latest

echo "Container started successfully."