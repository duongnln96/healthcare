#!/bin/sh

KAFKA_DIR=~/kafka_2.12-2.7.0
opt=$1
NUM_PARTITION=$2

INPUT_TOPIC="heart-disease-raw"
OUTPUT_TOPIC="heart-disease-out"
NUM_PARTITION_DEFAULT=1

if [[ ${opt} == "--help" ]]; then
    echo "Example command:"
    echo "./create-kafka-toipcs.sh IN | OUT"
fi

if [[ -z ${opt} ]]; then
    echo "Please fill topic in or out"
    exit 1
fi

if [[ -z ${NUM_PARTITION} ]]; then
    NUM_PARTITION=$NUM_PARTITION_DEFAULT
fi

if [[ ${opt} == "in" || ${opt} == "IN" ]]; then
    $KAFKA_DIR/bin/kafka-topics.sh --zookeeper localhost:2181 \
    --create --topic $INPUT_TOPIC \
    --partitions $NUM_PARTITION \
    --replication-factor 1
elif [[ ${opt} == "out" || ${opt} == "OUT" ]]; then
    $KAFKA_DIR/bin/kafka-topics.sh --zookeeper localhost:2181 \
    --create --topic $OUTPUT_TOPIC \
    --partitions $NUM_PARTITION \
    --replication-factor 1
fi
