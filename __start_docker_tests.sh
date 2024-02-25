#!/bin/bash

workdir="$(dirname "$0")"
image=homework-tests-img
container=homework-tests
port=8000

cd $workdir

echo -e "\n\n### Available docker images:"
docker image ls

echo -e "\n\n### Running docker images:"
docker ps

docker rm $container

echo -e "\n\n### Docker run (${image}) ..."
docker run --name $container -h $container -p $port:$port --volume=$workdir:/app $image
read -p "Press enter to continue"
