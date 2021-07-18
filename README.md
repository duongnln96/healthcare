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

#### **2. Producer and consumer**

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

## **Ref**

[1. Deeplearning4jPractical](https://www.dubs.tech/guides/quickstart-with-dl4j/#defining-a-schema)

[2. ModelTraining](https://deeplearning4j.konduit.ai/datavec/overview)

[3. Real-Time Remote Health Monitoring System Driven by 5G MEC-IoT](https://www.mdpi.com/2079-9292/9/11/1753)

[4. Benchmarking Apache Kafka](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines)
