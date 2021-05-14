#!/bin/bash

# export JMX_PORT=7081

java -javaagent:../shared-assets/prom-jmx/jmx_prometheus_javaagent-0.6.jar=1111:../shared-assets/prom-jmx/kafka_streams.yml \
	-jar ../analysis-service-java/target/healthcare-0.0.1-SNAPSHOT.jar