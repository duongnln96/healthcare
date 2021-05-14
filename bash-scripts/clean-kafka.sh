#!/bin/bash

KAFKA_LOGS_DIR=/tmp/kafka-logs
ZOOKEEPER_LOGS_DIR=/tmp/zookeeper

if [[ -d $KAFKA_LOGS_DIR ]]; then
	rm -rf $KAFKA_LOGS_DIR
fi

if [[ -d $ZOOKEEPER_LOGS_DIR ]]; then
	rm -rf $ZOOKEEPER_LOGS_DIR
fi
