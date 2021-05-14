#!/bin/bash

./run-zookeeper-server.sh stop 
./run-kafka-server.sh stop

if [[ "$1" == "clean" ]]; then
	./clean-kafka.sh
fi
