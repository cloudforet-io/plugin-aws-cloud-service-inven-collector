#!/usr/bin/env bash
RELATIVE_DIR=`dirname "$0"`
echo $RELATIVE_DIR

. $RELATIVE_DIR/build.sh
docker rm test_plugin
docker run -v "$(pwd)":/opt --name test_plugin pyengine/aws-cloud-services:1.0
# docker exec -ti test_plugin /bin/bash