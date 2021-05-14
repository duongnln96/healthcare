#!/bin/bash

KAFKA_DIR=~/kafka_2.12-2.7.0

opt=$1

if [ -z "${opt}"  ]; then
    echo "Please fill the action start or stop"
    exit 1
fi

if [[ ${opt} == "start" ]]; then
    $KAFKA_DIR/bin/zookeeper-server-$opt.sh -daemon $KAFKA_DIR/config/zookeeper.properties &
elif [[ ${opt} == "stop" ]]; then
    $KAFKA_DIR/bin/zookeeper-server-$opt.sh
fi

