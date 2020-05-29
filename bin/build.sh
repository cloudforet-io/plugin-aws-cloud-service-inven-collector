#!/usr/bin/env bash
# Build a docker image
docker build -t pyengine/aws-cloud-services . --no-cache
docker tag pyengine/aws-cloud-services pyengine/aws-cloud-services:1.1
docker tag pyengine/aws-cloud-services spaceone/aws-cloud-services:1.1
