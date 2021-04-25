#!/bin/sh

KAFKA_DIR=~/kafka_2.12-2.7.0
opt=$1

if [ -z "${opt}"  ]; then
    echo "Please fill the action start or stop"
    exit 1
fi

export KAFKA_OPTS="-javaagent:$KAFKA_DIR/prometheus/jmx_prometheus_javaagent-0.6.jar=7071:$KAFKA_DIR/prometheus/prom-jmx-agent-config.yml"
export JMX_PORT=7081

if [[ ${opt} == "start" ]]; then
    $KAFKA_DIR/bin/kafka-server-$opt.sh ./server-config.properties
elif [[ ${opt} == "stop" ]]; then
    $KAFKA_DIR/bin/kafka-server-$opt.sh
fi
