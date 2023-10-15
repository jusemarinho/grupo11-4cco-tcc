#!/bin/bash

if ! command -v docker &> /dev/null; then
    echo "Docker não está instalado. Por favor, instale o Docker antes de continuar."
    exit 1
fi

IMAGE_ID_APL_BACK_FRONT="49c5daab3213"
IMAGE_ID_MONGO="3222207ec48b"

docker run $IMAGE_ID_MONGO
docker run $IMAGE_ID_APL_BACK_FRONT
