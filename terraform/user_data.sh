#!/bin/bash

set -e

apt update -y
apt upgrade -y

apt install -y git docker.io docker-compose-v2

systemctl start docker
systemctl enable docker

usermod -aG docker ubuntu

mkdir -p /home/ubuntu/taskflow-deploy
chown -R ubuntu:ubuntu /home/ubuntu/taskflow-deploy