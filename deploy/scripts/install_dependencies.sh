# this makes sure that script runs on non-interative mode
export DEBIAN_FRONTEND=noninterative

sudo apt-get update-y
sudo apt-get install -y docker.io

sudo systemctl start docker
sudo systemctl enable docker

sudo apt-get install -y unzip curl

#download and install aws cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/home/ubuntu/awscliv2.zip"
unzip -o /home/ubuntu/awscliv2.zip -d /home/ubuntu
sudo /home/ubuntu/aws/install

# we are adding ubuntu user to the docker group to run docker commands without sudo
sudo usermod -aG docker ubuntu

#clean the aws cli installation files
rm -rf /home/ubuntu/awscliv2.zip /home/ubuntu/aws
