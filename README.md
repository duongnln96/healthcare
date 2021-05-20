# **HealthCare BigData**

## **Model**
[ColabNotebook](https://colab.research.google.com/drive/1C6rWrFjDEUCOjbubravx6ww8a9wqvd8t?usp=sharing)

## **Evaluate Performence**

### **Producer**

#### **Setup**

```console
$ ./bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic test1 --partitions 1 --replication-factor 1

$ ./bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic test2 --partitions 2 --replication-factor 1

$ ./bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic test3 --partitions 3 --replication-factor 1
```

#### **1. Single thread, async, no replication**

```console
./bin/kafka-run-class.sh org.apache.kafka.tools.ProducerPerformance \
--topic test1 \
--throughput -1 \
--num-records 5000000 \
--record-size 66560 \
--producer-props \
bootstrap.servers=localhost:9092 \
acks=1 \
```

#### **2. Effect of message size**

```bash
for i in 10 100 1000 10000 100000;
do
echo ""
echo $i
./bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance \
--topic test \
--throughput -1 \
--num-records $((1000*1024*1024/$i)) \
--record-size $i \
--producer-props \
bootstrap.servers=localhost:9092 \
acks=1 \
buffer.memory=67108864 batch.size=128000
done;
```

### **Consumer**

#### **1. Consumer throughput**

```console
./bin/kafka-consumer-perf-test.sh ----bootstrap-server localhost:9092 \
--messages 50000000 \
--topic test \
--threads 1
```

#### **2. Three Consumers**

On three servers, run:

```console
./bin/kafka-consumer-perf-test.sh ----bootstrap-server localhost:9092 \
--messages 50000000 \
--topic test \
--threads 1
```

#### **3. End-to-end Latency**

```console
./bin/kafka-run-class.sh kafka.tools.TestEndToEndLatency localhost:9092 localhost:2181 test 5000
```

#### **4. Producer and consumer**

```console
./bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance \
--topic test \
--throughput -1 \
--num-records 50000000 \
--record-size 200 \
--producer-props \
bootstrap.servers=localhost:9092 \
acks=1 \
buffer.memory=67108864 batch.size=8196

./bin/kafka-consumer-perf-test.sh --zookeeper localhost:2181 --messages 50000000 --topic test --threads 1
```


```console
$ ./bin/kafka-run-class.sh org.apache.kafka.tools.ProducerPerformance --help

usage: producer-performance [-h] --topic TOPIC --num-records NUM-RECORDS
                            [--payload-delimiter PAYLOAD-DELIMITER] --throughput THROUGHPUT
                            [--producer-props PROP-NAME=PROP-VALUE [PROP-NAME=PROP-VALUE ...]]
                            [--producer.config CONFIG-FILE] [--print-metrics]
                            [--transactional-id TRANSACTIONAL-ID]
                            [--transaction-duration-ms TRANSACTION-DURATION]
                            (--record-size RECORD-SIZE | --payload-file PAYLOAD-FILE)

This tool is used to verify the producer performance.

optional arguments:
  -h, --help             show this help message and exit
  --topic TOPIC          produce messages to this topic
  --num-records NUM-RECORDS
                         number of messages to produce
  --payload-delimiter PAYLOAD-DELIMITER
                         provides delimiter to be used  when  --payload-file is provided. Defaults
                         to new line. Note that this  parameter  will be ignored if --payload-file
                         is not provided. (default: \n)
  --throughput THROUGHPUT
                         throttle  maximum  message   throughput   to  *approximately*  THROUGHPUT
                         messages/sec. Set this to -1 to disable throttling.
  --producer-props PROP-NAME=PROP-VALUE [PROP-NAME=PROP-VALUE ...]
                         kafka producer related  configuration  properties like bootstrap.servers,
                         client.id etc. These configs  take  precedence  over  those passed via --
                         producer.config.
  --producer.config CONFIG-FILE
                         producer config properties file.
  --print-metrics        print out metrics at the end of the test. (default: false)
  --transactional-id TRANSACTIONAL-ID
                         The transactionalId to  use  if  transaction-duration-ms  is  > 0. Useful
                         when  testing  the  performance  of  concurrent  transactions.  (default:
                         performance-producer-default-transactional-id)
  --transaction-duration-ms TRANSACTION-DURATION
                         The max age of  each  transaction.  The  commitTransaction will be called
                         after this time has elapsed. Transactions  are only enabled if this value
                         is positive. (default: 0)

  either --record-size or --payload-file must be specified but not both.

  --record-size RECORD-SIZE
                         message size in bytes.  Note  that  you  must  provide  exactly one of --
                         record-size or --payload-file.
  --payload-file PAYLOAD-FILE
                         file to read  the  message  payloads  from.  This  works  only  for UTF-8
                         encoded text files. Payloads will be  read  from  this file and a payload
                         will be randomly  selected  when  sending  messages.  Note  that you must
                         provide exactly one of --record-size or --payload-file.

```
