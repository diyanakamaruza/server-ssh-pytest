#!/bin/bash

cd "$(dirname "$0")"

docker ps
docker image ls

read -p "This script will stop all docker container and prune (remove) them!! If you are really sure this is what you want to do, press enter to continue"
docker stop $(docker ps -a -q)
docker system prune -a -f

echo -e "\n\n### Docker build (homework-server}) ..."
docker build -f dockerfile-server.txt -t homework-server-img .

echo -e "\n\n### Docker build (homework-tests}) ..."
docker build -f dockerfile-tests.txt -t homework-tests-img .

docker image ls

read -p "Press enter to continue"

