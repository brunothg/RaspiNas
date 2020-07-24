#!/bin/bash

DOCKER_ID=$(sudo docker ps | grep nextcloud:fpm-alpine-custom | awk '{print $1}')
echo "Replace container with ID: $DOCKER_ID"

sudo docker stop "$DOCKER_ID"
sudo docker rm "$DOCKER_ID"

sudo docker pull nextcloud:fpm-alpine
sudo docker-compose up -d --build

